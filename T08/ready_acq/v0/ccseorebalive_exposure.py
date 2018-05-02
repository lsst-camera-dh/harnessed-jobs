###############################################################################
# REB aliveness exposure test
#
# Ex:
# source ts8setup-test
# [jh-test ts8prod@ts8-raft1 workdir]$ lcatr-harness --unit-type RTM --unit-id alive-test-1 --job rebalive_exposure --version v0
#
# author: homer    5/2016
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

if (True):
#attach CCS subsystem Devices for scripting
    ts8sub  = CCS.attachSubsystem("%s" % ts8);
    pwrsub  = CCS.attachSubsystem("ccs-rebps");
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
#    tssub  = CCS.attachSubsystem("%s" % ts);

    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
#    print "attaching Bias subsystem"
#    biassub   = CCS.attachSubsystem("%s/Bias" % ts);
#    print "attaching PD subsystem"
#    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
    print "attaching Mono subsystem"
    domono = True
    try:
        monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
    except:
        domono = False

    cdir = tsCWD

    ts_version = "NA"
    ts8_version = "NA"
    ts_revision = "NA"
    ts8_revision = "NA"

    fp = open("%s/rebalive_results_exposures.txt" % (cdir),"w");

    status_value = None

    wl = 500.
    if domono :
        for itry in range(3) :
            try:
                rwl = monosub.synchCommand(60,"setWaveAndFilter",wl).getResult();
                result = ts8sub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl,True)
                rply = monosub.synchCommand(900,"openShutter").getResult();
                break
            except:
                time.sleep(5.0)

#  Verify data link integrity.
    rebs = ""
    pstep = 1
    istep = 1
    test_name = "Step%d_REB_devices" % (pstep)
    try:
        result = ts8sub.synchCommand(10,"getREBDevices");
        rebs = result.getResult();
        status_value = rebs
    except:
        status_value = "failed"
    fp.write("%s| %s\n" % (test_name,status_value));

# ITL seq file
#    result = ts8sub.synchCommand(90,"loadSequencer","//home/ts8prod/workdir/sequencer-ts8-ITL-v7-etu2-pntr-explicit.seq");
#    result = ts8sub.synchCommand(90,"loadSequencer","//home/ts8prod/workdir/sequencer-ts8-ITL-v7-etu1-pntr-explicit.seq");
#    result = ts8sub.synchCommand(90,"loadSequencer",sequence_file);



    ccdnames = {}
    ccdmanunames = {}
    try:
        ccdnames["00"] = CCDS00
        ccdmanunames["00"] = CCDMANUS00
        ccdnames["01"] = CCDS01
        ccdmanunames["01"] = CCDMANUS01
        ccdnames["02"] = CCDS02
        ccdmanunames["02"] = CCDMANUS02
    except:
        pass
    try:
        ccdnames["10"] = CCDS10
        ccdmanunames["10"] = CCDMANUS10
        ccdnames["11"] = CCDS11
        ccdmanunames["11"] = CCDMANUS11
        ccdnames["12"] = CCDS12
        ccdmanunames["12"] = CCDMANUS12
    except:
        pass
    try:
        ccdnames["20"] = CCDS20
        ccdmanunames["20"] = CCDMANUS20
        ccdnames["21"] = CCDS21
        ccdmanunames["21"] = CCDMANUS21
        ccdnames["22"] = CCDS22
        ccdmanunames["22"] = CCDMANUS22
    except:
        pass

    rafttype = "ITL"
    raft = UNITID



    eolib.EOTS8Setup(tssub,ts8sub,pwrsub,raft,rafttype,cdir,sequence_file,vac_outlet)

    
#14. Execute a zero-second exposure and readout sequence. Start a timer when the close shutter command executes.

    ts8sub.synchCommand(10,"setDefaultImageDirectory","%s" % (cdir));

    if (True) :


        seqcmnd = "setSequencerStart Clear"
        print ts8sub.synchCommand(10,seqcmnd).getResult();
        for iclear in range(10):
            seqcmnd = "startSequencer"
            print "seqcmnd = (%s)" % seqcmnd
            print ts8sub.synchCommand(10,seqcmnd).getResult();
            time.sleep(1.0)


        expcmnd1 = 'exposeAcquireAndSave 100 True False ""'
        time.sleep(1.0)
            
        ts8sub.synchCommand(10,"setImageType BIAS")

        print "PRE-exposure command: expcmnd1 = ",expcmnd1
        print ts8sub.synchCommand(1500,expcmnd1).getResult() 


# <LSST CCD SN>_<test type>_<image type>_<seq. info>_<time stamp>.fits

#        fitsfilename = "s${sensorLoc}_r${raftLoc}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits"

#        print "fitsfilename = %s" % fitsfilename

        ts8sub.synchCommand(10,"setTestStand","TS6")
        ts8sub.synchCommand(10,"setTestType","FE55")

        raft = CCDID
#        ts8sub.synchCommand(10,"setRaftLoc",str(raft))

        exptime=0.0

        tm_start = time.time()
        print "Ready to take image with exptime = %f at time = %f" % (0,tm_start)

        ts8sub.synchCommand(10,"setTestType CONN")
        ts8sub.synchCommand(10,"setImageType BIAS")

        time.sleep(5.0)

# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",100,False,False,"${sensorLoc}_${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        tm_end = time.time()
        print "done taking image with exptime = %f at time = %f" % (0,tm_end)
        
        istep = istep + 1
        rebid = "raft"
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_start" % (istep,rebid),tm_start));
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_end" % (istep,rebid),tm_end));


        ts8sub.synchCommand(10,"setTestType CONN")
        ts8sub.synchCommand(10,"setImageType FLAT")

        exptime=1.000
        print "Doing 1000ms flat exposure"

        rply = ts8sub.synchCommand(120,"exposeAcquireAndSave",int(exptime*1000),True,False,"${sensorLoc}_${sensorId}_${test_type}_flat_1000ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        exptime=4.000
        print "Doing 4s Fe55 exposure"

        rply = ts8sub.synchCommand(280,"exposeAcquireAndSave",int(exptime*1000),False,True,"${sensorLoc}_${sensorId}_${test_type}_fe55_4000ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()

#        exptime=20.000
#
#        rply = ts8sub.synchCommand(280,"exposeAcquireAndSave",int(exptime*1000),True,True,"${sensorLoc}_${sensorId}_${test_type}_20000ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()


    fp.close();

# satisfy the expectations of ccsTools
    istate=0;
    fp = open("%s/status.out" % (cdir),"w");
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.close();


print "rebalive_functionalty test END"


###############################################################################               
# EOgetCCSVersions: getCCSVersions                                                            
def TS8getCCSVersions(ts8sub,cdir):
    result = ts8sub.synchCommand(10,"getCCSVersions");
    ccsversions = result.getResult()
    ccsvfiles = open("%s/ccsversion" % cdir,"w");
    ccsvfiles.write("%s" % ccsversions)
    ccsvfiles.close()

    ssys = ""

    ts8_version = ""
    ccsrebps_version = ""
    ts8_revision = ""
    ccsrebps_revision = ""
    for line in str(ccsversions).split("\t"):
        tokens = line.split()
        if (len(tokens)>2) :
            if ("ts8" in tokens[2]) :
                ssys = "ts8"
            if ("ccs-rebps" in tokens[2]) :
                ssys = "ccs-rebps"
            if (tokens[1] == "Version:") :
                print "%s - version = %s" % (ssys,tokens[2])
                if (ssys == "ts8") :
                    ts8_version = tokens[2]
                if (ssys == "ccs-rebps") :
                    ccsrebps_version = tokens[2]
            if (len(tokens)>3) :
                if (tokens[2] == "Rev:") :
                    print "%s - revision = %s" % (ssys,tokens[3])
                    if (ssys == "ts8") :
                        ts8_revision = tokens[3]
                    if (ssys == "ccs-rebps") :
                        ccsrebps_revision = tokens[3]

    return(ts8_version,ccsrebps_version,ts8_revision,ccsrebps_revision)
