###############################################################################
# monochromator calibration script
# Acquire qe images
#
###############################################################################

from org.lsst.ccs.scripting import *
from org.lsst.ccs.bus import CommandRejectedException
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

try:
#attach CCS subsystem Devices for scripting
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
    print "attaching Bias subsystem"
    biassub = CCS.attachSubsystem("%s/Bias" % ts);
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);

    time.sleep(3.)

    cdir = tsCWD

# Initialization
    print "doing initialization"

    print "Loading configuration file into the Archon controller"
    result = arcsub.synchCommand(20,"setConfigFromFile",acffile);
    reply = result.getResult();
    print "Applying configuration"
    result = arcsub.synchCommand(25,"applyConfig");
    reply = result.getResult();
    print "Powering on the CCD"
    result = arcsub.synchCommand(30,"powerOnCCD");
    reply = result.getResult();
    time.sleep(3.);

    print "past powering on the CCD"

#    print "Throwing away the first image"
#    arcsub.synchCommand(10,"setFitsFilename","");
#    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
#    reply = result.getResult();


    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");

    print "set expo to 1"

#    biassub.synchCommand(10,"setCurrentRange",0.000000002)
#    pdsub.synchCommand(10,"setCurrentRange",0.000002)
#    biassub.synchCommand(10,"setCurrentRange",0.000000002)
#    pdsub.synchCommand(10,"setCurrentRange",0.000002)
    biassub.synchCommand(10,"setCurrentRange",0.0000002)
    pdsub.synchCommand(10,"setCurrentRange",0.00002)

    print "set current ranges"

# move to TS acquisition state
    print "setting acquisition state"
#    result = tssub.synchCommand(60,"setTSTEST");
#    rply = result.getResult();


# get the glowing vacuum gauge off
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
#    rply = result.getResult();

#    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_LOLIM', default='1.0'))
#    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_HILIM', default='120.0'))
#    bcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_BCOUNT', default='1'))
#    imcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_IMCOUNT', default='1'))

    seq = 0

#number of PLCs between readings
    nplc = 1

    ccd = CCDID
    print "Working on CCD %s" % ccd

    monosub.synchCommand(60,"setTimeout",300.);

    print "set filter position"
    result = monosub.synchCommand(60,"setFilter",2);
    rply = result.getResult()
    result = monosub.synchCommand(60,"setSlitSize",1,420);
    rply = result.getResult()
    result = monosub.synchCommand(60,"setSlitSize",2,420);
    rply = result.getResult()

# go through config file looking for 'qe' instructions
    print "Scanning config file for LAMBDA specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

# take light exposures
    arcsub.synchCommand(10,"setParameter","Light","1");
    print "setting location of fits exposure directory"
    arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

#    wlstep = 323.
#    wl=500. - wlstep
#    for idx in range(2):
#        wl = wl + wlstep
#    for wl in [473.4, 473.4, 881.9, 881.9] :
    for wl in range(300,1100,10):

        exptime = 25.
        nreads = 3000
        arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# adjust timeout because we will be waiting for the data to become ready
        mywait = nplc/60.*nreads*1.10 ;
        print "Setting timeout to %f s" % mywait

        try:
#        monosub.synchCommand(30,"setWaveAndFilter",wl);
            print "Setting monochromator lambda = %8.2f" % wl
            try:
                result = monosub.synchCommand(200,"setWave",wl);
                rply = result.getResult()
                time.sleep(4.0)
            except CommandRejectedException, er:
                print "set wave attempt rejected, try again ..."
                time.sleep(10.0)
                try:
                    result = monosub.synchCommand(300,"setWave",wl);
                    rply = result.getResult()
                    time.sleep(4.0)
                except CommandRejectedException, er:
                    print "set wave attempt rejected again, one last try after a long wait again ..."
                    time.sleep(60.0)
                    try:
                        print "here we go ... its gotta work this time .... right?"
                        result = monosub.synchCommand(300,"setWave",wl);
                        rply = result.getResult()
                        print "we survived a near crash"
                        time.sleep(4.0)
                    except CommandRejectedException, et:
                        print "crash burn and live another step"
                        time.sleep(30.0)
                        continue
            result = monosub.synchCommand(300,"getWave");
            rwl = result.getResult()
        except ScriptingTimeoutException, ex:
            print "Failed to get monochromator to respond. Skipping to the next wavelength step."
            continue

        print "the wavelength read back is %f for seq %d" % (rwl,seq)
        print "publishing state"
        result = tssub.synchCommand(120,"getstate");
        stt = result.getResult()
        result = tssub.synchCommand(120,"setstate",stt);

        for i in range(1):
            print "starting acquisition step for lambda = %8.2f" % wl
# PD from PD setup
            print "Setup regular PD readout"
            pdsub.synchCommand(1000,"setTimeout",mywait);

            print "call accumBuffer to start PD recording at %f" % time.time()
            pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

            print "PD recording from PD device should now be in progress and the time is %f" % time.time()

# PD from BIAS setup
            print "Setup PD readout from Bias device"
            biassub.synchCommand(1000,"setTimeout",mywait);

            print "call accumBuffer to start PD recording from Bias device at %f" % time.time()
            pdbiasresult =  biassub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

            print "PD recording from Bias device should now be in progress and the time is %f" % time.time()

            time.sleep(10.)

# start acquisition
            timestamp = time.time()
            fitsfilename = "%s_lambda_%3.3d_%3.3d_lambda_%d_${TIMESTAMP}.fits" % ("mono_calib",int(wl),seq,i+1)
            arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
            result = arcsub.synchCommand(10,"setHeader","TestType","MonoCalib")

# make sure to get some readings before the state of the shutter changes       
            time.sleep(0.2);
 
            print "Ready to take image. time = %f" % time.time()
            result = arcsub.synchCommand(200,"exposeAcquireAndSave");
            fitsfilename = result.getResult();
            print "after click click at %f" % time.time()

            print "done with exposure # %d" % i
# readings from PD device
            print "getting photodiode readings from PD device at time = %f" % time.time();

            pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
            print "starting the wait for an accumBuffer done status message at %f" % time.time()
            tottime = pdresult.get();

# make sure the sample of the photo diode is complete
            time.sleep(10.)

            print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
#            pdrresult = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
            pdrresult = pdsub.asynchCommand("readBuffer","%s/%s" % (cdir,pdfilename));
#            buff = pdrresult.getResult()

# readings from PD device
            print "getting photodiode readings from Bias device at time = %f" % time.time();

            pdbiasfilename = "pdbias-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
            print "starting the wait for an accumBuffer done status message at %f" % time.time()
            tottime = pdbiasresult.get();

# make sure the sample of the photo diode is complete
#            time.sleep(30.)

            print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdbiasfilename)
            result = biassub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdbiasfilename));
            buff = result.getResult()
            print "Finished getting readings at %f" % time.time()

            buff = pdrresult.get()
            print "Finished getting readings at %f" % time.time()
# reset timeout to something reasonable for a regular command
#            pdsub.synchCommand(1000,"setTimeout",10.);
#            biassub.synchCommand(1000,"setTimeout",10.);

            result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
            result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdbiasfilename),fitsfilename,"AMP2.MEAS_TIMES","AMP2_MEAS_TIMES","AMP2_A_CURRENT",timestamp)

            fpfiles.write("%s %s/%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,cdir,pdbiasfilename,timestamp))

#            time.sleep(15.)

        seq = seq + 1

    fpfiles.close();
    fp.close();

    fp = open("%s/status.out" % (cdir),"w");

    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.close();

# move TS to idle state
                    
    tssub.synchCommand(60,"setTSReady");

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)


print "mono calib: END"
