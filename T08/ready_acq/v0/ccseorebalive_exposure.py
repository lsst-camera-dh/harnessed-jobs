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
    ts8sub  = CCS.attachSubsystem("ts8");
    pwrsub  = CCS.attachSubsystem("ccs-rebps");
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");


    cdir = tsCWD

    ts_version = "NA"
    ts8_version = "NA"
    ts_revision = "NA"
    ts8_revision = "NA"

    fp = open("%s/rebalive_results.txt" % (cdir),"w");

    status_value = None


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

    for i in range(2) :
#        fp.write("\n\nREB ID = %s\n" % rebid)
#        fp.write("==============================\n")

#13. Configure the ASPICs to standard gain and RC time constant, and leave the inputs in clamped state.

#        for i in range(6) :
#            ts8asp[i].synchCommand(10,"change clamp 1");


# Apply the CCD bias voltages and set the CCD clock rails (to E2V levels).                                               
#        result = ts8sub.synchCommand(90,"loadSequencer","seq_1M.xml");

# E2V seq file
#        result = ts8sub.synchCommand(90,"loadSequencer","/home/ts8prod/workdir/sequencer-reb3-model-geo2.seq");
 #        result = ts8sub.synchCommand(90,"loadSequencer","/home/ts8prod/workdir/sequencer-reb3-modelv2.seq");
# ITL seq file
        result = ts8sub.synchCommand(90,"loadSequencer","//home/ts8prod/workdir/sequencer-ts8-ITL-v6-pntr-explicit.seq");
 
#14. Execute a zero-second exposure and readout sequence. Start a timer when the close shutter command executes.

        ts8sub.synchCommand(10,"setDefaultImageDirectory","%s" % (cdir));

# <LSST CCD SN>_<test type>_<image type>_<seq. info>_<time stamp>.fits

        fitsfilename = "s${sensorLoc}_r${raftLoc}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits"

        print "fitsfilename = %s" % fitsfilename

        ts8sub.synchCommand(10,"setTestType","FE55")

        raft = CCDID
#        ts8sub.synchCommand(10,"setRaftLoc",str(raft))

        exptime=0.0

        tm_start = time.time()
        print "Ready to take image with exptime = %f at time = %f" % (0,tm_start)

        ts8sub.synchCommand(10,"setTestType CONN")
        ts8sub.synchCommand(10,"setImageType BIAS")

# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",0,False,False,"${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        tm_end = time.time()
        print "done taking image with exptime = %f at time = %f" % (0,tm_end)
        
        istep = istep + 1
        rebid = "raft"
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_start" % (istep,rebid),tm_start));
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_end" % (istep,rebid),tm_end));


        ts8sub.synchCommand(10,"setTestType CONN")
        ts8sub.synchCommand(10,"setImageType FLAT")

        exptime=0.100

        rply = ts8sub.synchCommand(120,"exposeAcquireAndSave",int(exptime*1000),True,True,"${sensorId}_${test_type}_100ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        exptime=4.000

        rply = ts8sub.synchCommand(120,"exposeAcquireAndSave",int(exptime*1000),True,True,"${sensorId}_${test_type}_4000ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        exptime=20.000

        rply = ts8sub.synchCommand(180,"exposeAcquireAndSave",int(exptime*1000),True,True,"${sensorId}_${test_type}_20000ms_${image_type}_${seq_info}_${timestamp}.fits").getResult()




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
