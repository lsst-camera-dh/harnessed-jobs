###############################################################################
# qe
# Acquire qe images
#
###############################################################################

from org.lsst.ccs.scripting import *
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
    biassub   = CCS.attachSubsystem("%s/Bias" % ts);
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

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,acffile,vac_outlet,arcsub,biassub,pdsub,pdusub)

    pdsub.synchCommand(10,"setCurrentRange",0.000002)

    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_HILIM', default='120.0'))
    bcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_BCOUNT', default='1'))
    imcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_IMCOUNT', default='1'))

    seq = 0

#number of PLCs between readings
    nplc = 1

    ccd = CCDID
    print "Working on CCD %s" % ccd

    print "set filter position"
    monosub.synchCommand(30,"setFilter",1); # open position

    arcsub.synchCommand(10,"setParameter","Fe55","0");

# clear the buffers
    print "doing some unrecorded bias acquisitions to clear the buffers"
    print "set controller for bias exposure"
    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","ExpTime","0");
    for i in range(5):
        timestamp = time.time()
        result = arcsub.synchCommand(10,"setFitsFilename","");
        print "Ready to take clearing bias image. time = %f" % time.time()
        result = arcsub.synchCommand(20,"exposeAcquireAndSave");
        rply = result.getResult()
        result = arcsub.synchCommand(500,"waitForExpoEnd");
        rply = result.getResult();


# go through config file looking for 'qe' instructions
    print "Scanning config file for LAMBDA specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'lambda')):
            wl = int(tokens[1])
            target = float(tokens[2])
            print "wl = %f" % wl;

            result = arcsub.synchCommand(10,"setHeader","SequenceNumber",seq)

            print "setting the monochromator wavelength to %f" % wl
#            if (exptime > lo_lim):
            result = monosub.synchCommand(500,"setWaveAndFilter",wl);
            rply = result.getResult()
            time.sleep(10.)
            try:
                result = monosub.synchCommand(200,"getWave");
                rwl = result.getResult()
            except ScriptingTimeoutException, ex:
                try:
                    print "failed once to do getWave ... try again"
                    time.sleep(10.)
                    result = monosub.synchCommand(200,"getWave");
                    rwl = result.getResult()
                except ScriptingTimeoutException, ex:
                    print "failed yet again to do getWave ... try one last time"
                    time.sleep(60.)
                    try:
                        result = monosub.synchCommand(200,"getWave");
                        rwl = result.getResult()
                    except ScriptingTimeoutException, ex:
                        print "ALERT ALERT ALERT ... SKIPPING A WAVELENGTH SETTING DUE TO NO wl RESPONSE FROM MONOCHROMATOR"
                        continue
            if (abs(wl-rwl)>1.0) :
                print "ALERT ALERT ALERT MONOCHROMATOR APPEARS NOT TO HAVE REACHED THE DESIRED WAVELENGTH"
                print "request wl = %f" % wl
                print "getwave returned wl = %f" % rwl
                print "SKIPPING THIS WAVELENGTH!"
                continue
            print "publishing state"
            result = tssub.synchCommand(60,"publishState");
            print "The wl retrieved from the monochromator is rwl = %f" % rwl
            result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)

# take bias images

            arcsub.synchCommand(10,"setParameter","ExpTime","0"); 
            arcsub.synchCommand(10,"setParameter","Light","0");

            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            result = arcsub.synchCommand(10,"setCCDnum",ccd)

            result = arcsub.synchCommand(10,"setHeader","TestType","LAMBDA")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
            for i in range(bcount):
                timestamp = time.time()
                fitsfilename = "%s_lambda_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)


# take light exposures
            arcsub.synchCommand(10,"setParameter","Light","1");
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));


# do in-job flux calibration
            arcsub.synchCommand(10,"setParameter","ExpTime","2000");

            result  = arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");
            result = arcsub.synchCommand(200,"exposeAcquireAndSave");
            flncal = result.getResult();
            result = arcsub.synchCommand(10,"getFluxStats",flncal);
            flux = float(result.getResult());

# scale 
#            flux = flux * 0.50

            exptime = target/flux
            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime

            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# prepare to readout diodes
            nreads = exptime*60/nplc + 60
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-60)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            result = arcsub.synchCommand(10,"setHeader","TestType","LAMBDA")
            result = arcsub.synchCommand(10,"setHeader","ImageType","FLAT")


# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*1.10 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            for i in range(imcount):
                print "starting acquisition step for lambda = %8.2f" % wl

                print "call accumBuffer to start PD recording at %f" % time.time()
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition
                timestamp = time.time()
                fitsfilename = "%s_lambda_flat_%3.3d_%3.3d_%d_${TIMESTAMP}.fits" % (ccd,int(wl),seq,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                print "fitsfilename = %s" % fitsfilename

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.5);

                print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i
                print "getting photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
#                time.sleep(10.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()



                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
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
    fp.write("%s\n" % archon_version);
    fp.write("%s\n" % archon_revision);
    fp.close();

# move TS to idle state
                    
    tssub.synchCommand(60,"setTSReady");

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

except Exception, ex:

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)


print "QE: END"
