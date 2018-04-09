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

from org.lsst.ccs.scripting import *
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

# get REB device list
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

# load the sequencer redimensioned for scan mode
    result = ts8sub.synchCommand(90,"enableScan true");
    result = ts8sub.synchCommand(90,"loadSequencerAndReDimension %s 48 1000 1000 100 256 220",sequence_file);



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
# clearing
        seqcmnd = "setSequencerStart Clear"
        print ts8sub.synchCommand(10,seqcmnd).getResult();
        for iclear in range(10):
            seqcmnd = "startSequencer"
            print "seqcmnd = (%s)" % seqcmnd
            print ts8sub.synchCommand(10,seqcmnd).getResult();
            time.sleep(1.0)
        expcmnd1 = 'exposeAcquireAndSave 0 True False ""'
        time.sleep(1.0)
        ts8sub.synchCommand(10,"setImageType BIAS")
        print "PRE-exposure command: expcmnd1 = ",expcmnd1
        print ts8sub.synchCommand(1500,expcmnd1).getResult() 

# --------
        ts8sub.synchCommand(10,"setTestStand","TS6")
        raft = CCDID
        exptime=1.0

# TM mode
        print "setting transparent mode(tm) for ASPICs"
        ts8asp = [0,0,0,0,0,0,0,0]
        for i in range(6) :
            ts8asp[i] = CCS.attachSubsystem("%s/%s.ASPIC%d" % (ts8,rebid,i))
            result = ts8asp[i].synchCommand(10,"change tm 1")

        print "loading ASPICS"

        try:
            result = ts8sub.synchCommand(10,"loadAspics true");
            status_value = result.getResult();
        except:
            print "command failure!"
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));
# exposure
        tm_start = time.time()
        print "Ready to take image with exptime = %f at time = %f" % (0,tm_start)
        ts8sub.synchCommand(10,"setTestType SCAN_TM")
        ts8sub.synchCommand(10,"setImageType FLAT")
# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",int(exptime*1000.0),False,False,"${sensorLoc}_${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}_scan_mode_tm.fits").getResult()
        time.sleep(15.0)

        tm_end = time.time()
        print "done taking image with exptime = %f at time = %f" % (exptime,tm_end)

# DSI mode
        print "setting transparent mode(tm) for ASPICs"
        ts8asp = [0,0,0,0,0,0,0,0]
        for i in range(6) :
            ts8asp[i] = CCS.attachSubsystem("%s/%s.ASPIC%d" % (ts8,rebid,i))
            result = ts8asp[i].synchCommand(10,"change tm 0")

        print "loading ASPICS"

        try:
            result = ts8sub.synchCommand(10,"loadAspics true");
            status_value = result.getResult();
        except:
            print "command failure!"
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));
# exposure
        tm_start = time.time()
        print "Ready to take image with exptime = %f at time = %f" % (0,tm_start)
        ts8sub.synchCommand(10,"setTestType SCAN_DSI")
        ts8sub.synchCommand(10,"setImageType FLAT")
# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",int(exptime*1000.0),False,False,"${sensorLoc}_${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}_scan_mode_dsi.fits").getResult()
        time.sleep(15.0)

        tm_end = time.time()
        print "done taking image with exptime = %f at time = %f" % (exptime,tm_end)
        



    fp.close();

    result = ts8sub.synchCommand(90,"enableScan false");
    result = ts8sub.synchCommand(90,"loadSequencer %s",sequence_file);

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
