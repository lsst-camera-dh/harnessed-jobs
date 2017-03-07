###############################################################################
# flat
# Acquire flat image pairs for linearity and gain measurement.
# For each 'flat' command a pair of flat field images are acquired
#
# In the configuration file the format for a flat command is
# flat   signal  
# where signal is the desired acquired signal level in e-/pixel
#
# FLAT_WL is used to determine what wavelength will be used for illumination
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

    print "initializing archon controller with file %s" % acffile
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

    print "set controller parameters for an exposure with the shutter closed"
#    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");

# the first image is usually bad so throw it away
    print "Throwing away the first image"
    arcsub.synchCommand(10,"setFitsFilename","");
    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
    reply = result.getResult();
    
# move to TS acquisition state
    print "setting acquisition state"
    result = tssub.synchCommand(60,"setTSTEST");
    rply = result.getResult();

#check state of ts devices
    print "wait for ts state to become ready";
    tsstate = 0
    starttim = time.time()
    while True:
        print "checking for test stand to be ready for acq";
        result = tssub.synchCommand(10,"isTestStandReady");
        tsstate = result.getResult();
# the following line is just for test situations so that there would be no waiting
        tsstate=1;
        if ((time.time()-starttim)>240):
            print "Something is wrong ... we will never make it to a runnable state"
            exit
        if tsstate!=0 :
            break
        time.sleep(5.)
#put in acquisition state
    print "We are ready to go! Ramping the BP bias voltage now."
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

# get the glowing vacuum gauge off
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
    rply = result.getResult();

    print "Now collect some parameters from the config file"
    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'FLAT_LOLIM', default='0.1'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'FLAT_HILIM', default='120.0'))
    bcount = float(eolib.getCfgVal(acqcfgfile, 'FLAT_BCOUNT', default = "2"))
    wl     = float(eolib.getCfgVal(acqcfgfile, 'FLAT_WL', default = "550.0"))
    imcount = 2

#number of PLCs between readings
    nplc = 1

    seq = 0  # image pair number in sequence

    monosub.synchCommand(30,"setFilter",1);


    ccd = CCDID
    print "Working on CCD %s" % ccd

# go through config file looking for 'flat' instructions, take the flats
    print "Scanning config file for FLAT specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    owl = 0.
    flux = 0.

    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'flat')):

            target = float(tokens[1])

            print "target exposure = %d" % (target);

#            exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)

# take bias images
            print "set controller for bias exposure"
            arcsub.synchCommand(10,"setParameter","Light","0");
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
 
            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

 
            print "start bias exposure loop"

            result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
            for i in range(bcount):
                timestamp = time.time()

                print "set fits filename"
                fitsfilename = "%s_flat_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)

# take light exposures
            arcsub.synchCommand(10,"setParameter","Light","1");
#            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "setting the monochromator wavelength"
#            if (exptime > lo_lim):

            if (wl!=owl) :
                result = monosub.synchCommand(200,"setWaveAndFilter",wl);
                rply = result.getResult()
                time.sleep(4.)
                result = monosub.synchCommand(200,"getWave");
                rwl = result.getResult()
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");

# do in-job flux calibration
                exp1 = 1.0
                exp2 = 2.0

# use two exposures of different exposure times to determine flux
# first
                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exp1*1000)));

                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                rply = result.getResult();
                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");

                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                flncal = result.getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                fl1 = float(result.getResult());
# second
                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exp2*1000)));

                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                rply = result.getResult();
                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");

                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                flncal = result.getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                fl2 = float(result.getResult());

                flux = ((fl2*exp2)-(fl1*exp1))/(exp2-exp1)
                print "fluxcalc: exp1 = %f, fl1 = %f, exp2 = %f, fl2 = %f  ==> flux = %f" % (float(exp1),float(fl1),float(exp2),float(fl2),float(flux))
                owl = wl

            exptime = target/flux
            print "for target signal %f, the exposure time = %f" % (target,exptime)
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc
                
            result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","FLAT")

            print "Throwing away the first image"
            arcsub.synchCommand(10,"setFitsFilename","");
            result = arcsub.synchCommand(200,"exposeAcquireAndSave");
            reply = result.getResult();
            time.sleep(exptime)

# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*1.10 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            print "starting acquisition step for lambda = %8.2f with exptime %8.2f s" % (wl, exptime)

            for i in range(imcount):

                print "nreads set to %d and nplc set to %f" % (int(nreads),float(nplc))
                pdresult = pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);
                timestamp = time.time()

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.2);

# start acquisition
                print "set fits filename"
                fitsfilename = "%s_flat_%3.3d_%3.3d_flat%d_${TIMESTAMP}.fits" % (ccd,int(wl),seq,i+1)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i
                print "getting photodiode readings"

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)

# the primary purpose of this is to guarantee that the accumBuffer method has completed
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(5.)
 
                print "executing readBuffer"
                try:
                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                except:
# give it one more try
                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()

                print "Finished getting readings at %f" % time.time()

                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))
# -----------end of imcount loop -------------------
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
    
    fp.close();

# move TS to idle state
                    
    tssub.synchCommand(60,"setTSReady");
# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "FLAT: END"
