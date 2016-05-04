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

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""


  
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
