###############################################################################
# qe
# Acquire qe images for RAFT EO testing at TS8
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
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
    print "attaching Bias subsystem"
    biassub   = CCS.attachSubsystem("%s/Bias" % ts);
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "Attaching ts8 subsystem"

    ts8sub  = CCS.attachSubsystem("ts8");

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""


# get the software versions to include in the data products to be persisted in the DB
#    ts_version,ts8_version,ts_revision,ts8_revision = eolib.EOgetCCSVersions(tssub,cdir)

# prepare TS8: make sure temperature and vacuum are OK and load the sequencer
#    eolib.EOSetup(tssub,RAFTID,CCSRAFTTYPE,cdir,sequence_file,vac_outlet,ts8sub)
  
    result = ts8sub.synchCommand(90,"loadSequencer",acffile);


    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_HILIM', default='120.0'))
    bcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_BCOUNT', default='1'))
    imcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_IMCOUNT', default='1'))

    bcount = 3

    seq = 0

#number of PLCs between readings
    nplc = 1.0

#    raft = RAFTID
    raft = CCDID
    print "Working on RAFT %s" % raft

# options:exposure_time, open_shutter, actuate_xed, file_pattern
# make sure the XED is deactivated
#    ts8sub.synchCommand(10,"setExposureParameter","Fe55","0");
#    ts8sub.synchCommand(30,"setExposureParameter","actuate_xed","False");


# clear the REB buffers
#    ,,, is this still needed?


# go through config file looking for 'qe' instructions
    print "Scanning config file for LAMBDA specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'lambda')):
            wl = int(tokens[1])

# Note: stop it at 500 ... this is just for demonstration purposes for now
            if (wl > 350.) :
                break

            target = float(tokens[2])
            print "wl = %f" % wl;

#            result = ts8sub.synchCommand(10,"setHeader","SequenceNumber",str(seq),False)
# Note:
#ts8 ccs>setHeader test ExpTime 1.0
#*** Failed to invoke main method in class org.lsst.ccs.subsystem.shell.ConsoleCommandShell
#*** Reason:  Error finding command setHeader with 3 arguments: 2 matches found in MethodBasedCommandDictionary
#[jh-test ts8prod@ts8-raft1 workdir]$ 

            print "setting the monochromator wavelength to %f" % wl

            result = monosub.synchCommand(1000,"setWaveAndFilter",wl);
            rwl = result.getResult()
            time.sleep(10.)
            if (abs(wl-rwl)>1.0) :
                print "ALERT ALERT ALERT MONOCHROMATOR APPEARS NOT TO HAVE REACHED THE DESIRED WAVELENGTH"
                print "request wl = %f" % wl
                print "getwave returned wl = %f" % rwl
                print "SKIPPING THIS WAVELENGTH!"
                continue
            print "publishing state"
            result = tssub.synchCommand(60,"publishState");
            print "The wl retrieved from the monochromator is rwl = %f" % rwl
#            result = ts8sub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)

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
            result = ts8sub.synchCommand(90,"loadSequencer",acffile);

# probably not needed any more ... reduce count to 1
            for i in range(1):
                timestamp = time.time()
                ts8sub.synchCommand(10,"setExposureParameter exposure_time 0"); 
                ts8sub.synchCommand(10,"setFitsFilesNamePattern","clear.fits");
                print "Ready to take clearing bias image. time = %f" % time.time()
                ts8sub.synchCommand(50,"exposeAcquireAndSave");
#                Note: How to wait for a response
#                fitsfilename = result.getResult();
#                result = ts8sub.synchCommand(500,"waitForExpoEnd");
#                rply = result.getResult();
                print "after click click at %f" % time.time()

            time.sleep(3.0)

            for i in range(bcount):
                timestamp = time.time()
                ts8sub.synchCommand(10,"setExposureParameter exposure_time 0"); 
#                fitsfilename = "%s_lambda_bias_%3.3d_${TIMESTAMP}.fits" % (raft,seq)
                fitsfilename = "%s_lambda_bias_%3.3d_%s.fits" % (raft,seq,time.time())
                ts8sub.synchCommand(10,"setFitsFilesNamePattern",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                result = ts8sub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
#                result = ts8sub.synchCommand(500,"waitForExpoEnd");
#                rply = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(3.0)


# take light exposures
#            ts8sub.synchCommand(10,"setExposureParameter","Light","1");
            print "setting location of fits exposure directory"
            ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));
            ts8sub.synchCommand(10,"setFitsFilesNamePattern","clear.fits");
            ts8sub.synchCommand(10,"setExposureParameter exposure_time 2000"); 

            ts8sub.synchCommand(50,"exposeAcquireAndSave");
#            fitsfilename = result.getResult();
#            result = ts8sub.synchCommand(500,"waitForExpoEnd");
#            rply = result.getResult();
            print "after click click at %f" % time.time()
            time.sleep(2.0)

# do in-job flux calibration
# QUESTION: how do we want this to choose a value for a set of sensors?

#            result  = ts8sub.synchCommand(10,"setFitsFilesNamePattern","fluxcalimage-${TIMESTAMP}");
            ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));
            ts8sub.synchCommand(10,"setExposureParameter exposure_time 2000"); 
            ts8sub.synchCommand(10,"setFitsFilesNamePattern","fluxcalimage-%s" % time.time());
            ts8sub.synchCommand(200,"exposeAcquireAndSave");
# Note: since I don't know how to wait
            time.sleep(2.0)
#            flncal = result.getResult();
#            result = ts8sub.synchCommand(500,"waitForExpoEnd");
#            rply = result.getResult();
 
#            result = ts8sub.synchCommand(10,"getFluxStats",flncal);
#            flux = float(result.getResult());
# force it to a fixed value for now 
            flux = 2000.0

            time.sleep(2.0)

# scale 
#            flux = flux * 0.50

            exptime = target/flux
#            exptime = 10000
            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime



# prepare to readout diodes
            if (exptime>0.5) :
                nplc = 1.0
            else :
                nplc = 0.25

# Note: for testing, make these recordings as quick as possible by reducing the number of samples:
#            nplc = nplc * 10

            nreads = (exptime+2.0)*60/nplc
            if (nreads > 3000):
                nreads = 3000
                nplc = (exptime+2.0)*60/nreads
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA",False)
            ts8sub.synchCommand(10,"setHeader","ImageType","FLAT",False)


# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*2.00 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

#            ts8sub.synchCommand(10,"setExposureParameter exposure_time %s" % str(int(exptime*1000)));
            print "setExposureParameter exposure_time %s" % str(int(exptime*1000))
            ts8sub.synchCommand(10,"setExposureParameter exposure_time 10000");

            print "Ready to take clearing bias image. time = %f" % time.time()
            ts8sub.synchCommand(10,"setExposureParameter open_shutter false");
            print "setting location of bias fits directory"
            ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));
            ts8sub.synchCommand(10,"setFitsFilesNamePattern","clear.fits");

            ts8sub.synchCommand(300,"exposeAcquireAndSave");
# Note: since I don't know how to wait
            time.sleep(exptime)

#            rply = result.getResult()
#            result = ts8sub.synchCommand(500,"waitForExpoEnd");
#            rply = result.getResult();

#            time.sleep(4.0)

            result = ts8sub.synchCommand(90,"loadSequencer",acffile);

            for i in range(imcount):
                print "image number = %d" % i
                print "starting acquisition step for lambda = %8.2f" % wl

                print "call accumBuffer to start PD recording at %f" % time.time()
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                while(True) :
                    result = pdsub.synchCommand(10,"isAccumInProgress");
                    rply = result.getResult();
                    print "checking for PD accumulation in progress at %f" % time.time()
                    if rply==True :
                        print "accumulation running"
                        break
                    print "accumulation hasn't started yet"
                    time.sleep(0.25)
                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition
                timestamp = time.time()

                print "setExposureParameter exposure_time %s" % str(int(exptime*1000))
                ts8sub.synchCommand(10,"setExposureParameter exposure_time 10000");
                ts8sub.synchCommand(10,"setExposureParameter open_shutter true");
                ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));

#                fitsfilename = "%s_lambda_flat_%4.4d_%3.3d_${TIMESTAMP}.fits" % (ts8,int(wl),seq)
                fitsfilename = "%s_lambda_flat_%4.4d_%3.3d_%s.fits" % (raft,int(wl),seq,time.time())
                ts8sub.synchCommand(10,"setFitsFilesNamePattern",fitsfilename);
                print "fitsfilename = %s" % fitsfilename

# make sure to get some readings before the state of the shutter changes       
                time.sleep(1.0);

                print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())
                ts8sub.synchCommand(500,"exposeAcquireAndSave");
# Note: since I don't know how else to wait
                time.sleep(exptime)

#                fitsfilename = result.getResult();
#                result = ts8sub.synchCommand(500,"waitForExpoEnd");
#                rply = result.getResult();
                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i
                print "getting photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(2.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
# Note: otherwise it will try to write to a directory that doesn't exist on the other machine
#                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                result = pdsub.synchCommand(1000,"readBuffer","/tmp/%s" % pdfilename);
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()


# Note: note implemented yet
#                result = ts8sub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))
# ------------------- end of imcount loop --------------------------------
# reset timeout to something reasonable for a regular command
            pdsub.synchCommand(1000,"setTimeout",10.);
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

# move TS to idle state
                    
#    result = tssub.synchCommand(200,"setTSReady");
#    rply = result.getResult();

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
try:
    result = ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA-END",False)
    print "something"

except Exception, ex:

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)


print "QE: END"
