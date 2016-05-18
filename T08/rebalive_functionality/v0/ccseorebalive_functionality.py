###############################################################################
# REB aliveness functionality test
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

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""

    fp = open("%s/rebalive_report.results" % (cdir),"w");

# attempt to power apply the REB power
    test_name = "apply_power"
    try:
        result = pwrsub.synchCommand(10,"togglePower");
        status_value = "success";
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value);

#  Verify data link integrity.
    test_name = "link_integrity"
    try:
        result = ts8sub.synchCommand(10,"getREBDevices");
        status_value = result.getResult();
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value);

# Read 1-wire ID chip and record the value.
    test_name = "link_integrity"
    try:
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.6Vi");
        fitsfilename = result.getResult();
        status_value = "success"
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value);

# Read and record the REB firmware version.
# see: https://confluence.slac.stanford.edu/display/LSSTCAM/REB+Register+Sets
    test_name = "REB_firmware_version"
    try:
        result = ts8sub.synchCommand(10,"readRegister 0");
        fitsfilename = result.getResult();
        status_value = "success"
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value);


# Read the voltage and current consumption measured by the VP5 LTC2945 current monitor on the REB, record the value and compare to the current measured at the P/S.
    try:
        test_name = "VP5_LTC2945_6V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.6Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.6Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_9V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.9Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.9Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_24V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.24Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.24Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_40V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.40Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.40Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

    except:
        test_name = "VP5_LTC2945"
        status_value = "failed"


# Apply the analog power supply voltages (VP15_UNREG, VN15_UNREG, VP7_UNREG, VP40_UNREG) to the REB in the correct sequence (check with Rick for sequence and voltage values). Abort the test if any supply hits it overcurrent limit. Readback voltages and current consumption at the P/S and at the REB LTC2945 sensors.

    try:
        test_name = "VP5_LTC2945_6V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.6Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.6Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_9V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.9Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.9Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_24V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.24Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.24Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

        test_name = "VP5_LTC2945_40V_I"
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.40Vv");
        rebv =  = result.getResult();
        result = ts8sub.synchCommand(10,"getChannelValue DR00.Reb0.40Vi");
        rebi  = result.getResult();
        fp.write("%-20s\t | \t %f \t %f\n" % (test_name,rebv, rebi);

    except:
        test_name = "VP5_LTC2945"
        status_value = "failed"



#ccs-rebps/sequencePower  ? ?  Ideally yes, but currently ccs-rebps togglePower
#ccs-rebps/MainPS getCurrent    ccs-rebps readChannelValue

# Verify that all currents are within the expected range 


# Record the value of the currents on each supply, both at the P/S and by the REB.


# Readback the temperatures measured by each of the ADT7420 sensors on the REB.


# Apply the CCD bias voltages and set the CCD clock rails (to E2V levels).

ccs-rebps/setBiasDac ?  ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs

12. Re-check supply currents and verify they do not exceed expected values.
13. Configure the ASPICs to standard gain and RC time constant, and leave the inputs in
clamped state.

ccs-rebps/sequencePower  ? ?  ccs-rafts loadAspics

14. Execute a zero-second exposure and readout sequence. Start a timer when the \u201cclose
shutter\u201d command executes.
loadSequencer ...

setExposureParameter open_shutter false
setExposureParameter exposure_time 0
exposeAcquireAndSave

(I am purposely skipping the directory and filename settings)

  
    result = ts8sub.synchCommand(90,"loadSequencer",acffile);

    raft = CCDID
    print "Working on RAFT %s" % raft

#
# take bias images
# 

    ts8sub.synchCommand(10,"setExposureParameter open_shutter false");

    print "setting location of bias fits directory"
    ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));

#            result = ts8sub.synchCommand(10,"setRaftName",raft)
# Note: throws a not implemented exception

    ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA",False)
    ts8sub.synchCommand(10,"setHeader","ImageType","BIAS",False)

    for i in range(2):
        timestamp = time.time()
        ts8sub.synchCommand(10,"setExposureParameter exposure_time 0"); 

        fitsfilename = "%s_lambda_bias_%3.3d_%s.fits" % (raft,seq,time.time())
        ts8sub.synchCommand(10,"setFitsFilesNamePattern",fitsfilename);
        
        print "Ready to take bias image. time = %f" % time.time()
        result = ts8sub.synchCommand(500,"exposeAcquireAndSave");
        fitsfilename = result.getResult();



# take light exposures
#            ts8sub.synchCommand(10,"setExposureParameter","Light","1");
            ts8sub.synchCommand(10,"setExposureParameter open_shutter true");

            ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA",False)
            ts8sub.synchCommand(10,"setHeader","ImageType","FLAT",False)


            print "setExposureParameter exposure_time %s" % str(int(exptime*1000))
            ts8sub.synchCommand(10,"setExposureParameter exposure_time 10000");

            for i in range(imcount):
                print "image number = %d" % i
# start acquisition
                timestamp = time.time()

                print "setExposureParameter exposure_time %s" % str(int(exptime*1000))
                ts8sub.synchCommand(10,"setExposureParameter exposure_time 10000");
                ts8sub.synchCommand(10,"setExposureParameter open_shutter true");
                ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));

                fitsfilename = "%s_lambda_flat_%4.4d_%3.3d_%s.fits" % (raft,int(wl),seq,time.time())
                ts8sub.synchCommand(10,"setFitsFilesNamePattern",fitsfilename);
                print "fitsfilename = %s" % fitsfilename

                print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())
                ts8sub.synchCommand(500,"exposeAcquireAndSave");

            seq = seq + 1

    fpfiles.close();
    fp.close();

    fp = open("%s/status.out" % (cdir),"w");

    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.close();

try:
    result = ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA-END",False)
    print "something"

except Exception, ex:


    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)


print "rebalive_functionalty test END"
