###############################################################################
# flat
# Acquire flat image pairs for linearity measurement.
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

    eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)

    print "Setting the current ranges on the Bias and PD devices"
    pdsub.synchCommand(10,"setCurrentRange",0.000002)

    print "Now collect some parameters from the config file"
    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'FLAT_LOLIM', default='0.1'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'FLAT_HILIM', default='120.0'))
    bcount = float(eolib.getCfgVal(acqcfgfile, 'FLAT_BCOUNT', default = "2"))
    wl     = float(eolib.getCfgVal(acqcfgfile, 'FLAT_WL', default = "550.0"))
    imcount = 2

#number of PLCs between readings
    nplc = 1

    seq = 0  # image pair number in sequence

    ccd = CCDID
    print "Working on CCD %s" % ccd

    arcsub.synchCommand(10,"setParameter","Fe55","0");

    result = monosub.synchCommand(30,"setSlitSize",1,210);
    result = monosub.synchCommand(30,"setSlitSize",2,210);

# clear the buffers                                                                                          
    print "doing some unrecorded bias acquisitions to clear the buffers"
    print "set controller for bias exposure"
    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","ExpTime","0");
    arcsub.synchCommand(10,"setParameter","WaiTime","200");
    for i in range(5):
        timestamp = time.time()
        result = arcsub.synchCommand(10,"setFitsFilename","");
        print "Ready to take clearing bias image. time = %f" % time.time()
        result = arcsub.synchCommand(120,"exposeAcquireAndSave");
        rply = result.getResult()
        print "waiting for exposure to complete"
        time.sleep(0.2)
        result = arcsub.synchCommand(500,"waitForExpoEnd");
        rply = result.getResult();
        print "done, ready for next one"


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

            result = arcsub.synchCommand(10,"setHeader","SequenceNumber",seq)

#            exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)

# take bias images
            print "set controller for bias exposure"
            arcsub.synchCommand(10,"setParameter","Light","0");
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
 
            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "start bias exposure loop"

            result = arcsub.synchCommand(10,"setCCDnum",ccd)
            result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

            for i in range(2):
                timestamp = time.time()
                arcsub.synchCommand(10,"setFitsFilename","");
                print "Ready to take clearing bias image. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                print "after click click at %f" % time.time()

            for i in range(bcount):
                timestamp = time.time()

                print "set fits filename"
                fitsfilename = "%s_flat_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();

                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                print "after click click at %f" % time.time()

                time.sleep(1.0)
# ===========================================================================
#            time.sleep(2.0)

# take light exposures
            arcsub.synchCommand(10,"setParameter","Light","1");

            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            if (wl!=owl) :
                print "Setting monochromator lambda = %8.2f" % wl
                result = monosub.synchCommand(60,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.0)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");
                result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)

# do in-job flux calibration
# #####################################################################################3
# dispose of first image
                arcsub.synchCommand(10,"setParameter","Light","1");
                arcsub.synchCommand(10,"setParameter","ExpTime","2000");
                
                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                
                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                
                time.sleep(2.0)
                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                rply = result.getResult();
                
                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");
            
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                flncal = result.getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                flux = float(result.getResult());

                print "The flux is determined to be %f" % flux

                owl = wl
# ####################################################################################3
            exptime = target/flux
            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime
#            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# prepare to readout diodes
            if (exptime>0.5) :
                nplc = 1.0
            else :
                nplc = 0.20

            nreads = (exptime+5.0)*60/nplc
            if (nreads > 3000):
                nreads = 3000
                nplc = (exptime+4.0)*60/nreads
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc
                
            result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","FLAT")


# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*2.00 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            print "starting acquisition step for lambda = %8.2f with exptime %8.2f s" % (wl, exptime)

# ##########################################################################################
            print "throw away first image"
# wait an amount of time equivalent to the last flux image taken
#            time.sleep(2.0)
            arcsub.synchCommand(10,"setParameter","Light","1");
#            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
#            result = arcsub.synchCommand(10,"setFitsFilename","");
#            print "Ready to take disposable image. time = %f" % time.time()
#            result = arcsub.synchCommand(500,"exposeAcquireAndSave");
#            fitsfilename = result.getResult();
#            result = arcsub.synchCommand(500,"waitForExpoEnd");
#            rply = result.getResult();
#            print "done waiting for throw away image to be acquired %f" % time.time()
#            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
# ##########################################################################################
            for i in range(imcount):

# take bias image
                print "set controller for bias exposure"
                arcsub.synchCommand(10,"setParameter Nexpo 1");
                arcsub.synchCommand(10,"setParameter","Light","0");
                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
                result = arcsub.synchCommand(10,"setCCDnum",ccd)
                result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
                for ii in range(1):
                    arcsub.synchCommand(10,"setFitsFilename","");
                    print "Ready to take clearing bias image. time = %f" % time.time()
                    result = arcsub.synchCommand(500,"exposeAcquireAndSave").getResult();
                    result = arcsub.synchCommand(500,"waitForExpoEnd").getResult();


####### just added - 2017/02/20
                print "doing some unrecorded acquisitions to clear the buffers"

                arcsub.synchCommand(10,"setParameter Nexpo 1");
                arcsub.synchCommand(10,"setParameter","Light","1");
                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
                arcsub.synchCommand(10,"setParameter","WaiTime","200");
                for ii in range(1):
                    timestamp = time.time()
                    result = arcsub.synchCommand(10,"setFitsFilename","");
                    print "Ready to take pre-image. time = %f" % time.time()
                    rply = arcsub.synchCommand(120,"exposeAcquireAndSave").getResult();
                    print "waiting for exposure to complete"
                    time.sleep(0.2)
                    rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();
                    print "done, ready for next one"



                print "starting image setup and PD reading accumulation at %f" % time.time()
                print "nreads set to %d and nplc set to %f" % (int(nreads),float(nplc))
                pdresult = pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

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

                timestamp = time.time()

# make sure to get some readings before the state of the shutter changes       
#                time.sleep(1.0);

# start acquisition
                print "set fits filename"
#                fitsfilename = "%s_flat_%4.4d_%4.4d_flat%d_${TIMESTAMP}.fits" % (ccd,int(exptime*1000),seq,i+1)
                fitsfilename = "%s_flat_%07.2f_flat%d_${TIMESTAMP}.fits" % (ccd,exptime,i+1)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take image. time = %f" % time.time()
# set exptime just before exposure
                fitsfilename = arcsub.synchCommand(500,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();
                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i

# set for continuous unrecord bias image
                result = arcsub.synchCommand(10,"setFitsFilename","");
                arcsub.synchCommand(10,"setParameter Nexpo 100000");
                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                arcsub.synchCommand(10,"setParameter","WaiTime","200");
                rply = arcsub.synchCommand(500,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

                print "getting photodiode readings"

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)

# the primary purpose of this is to guarantee that the accumBuffer method has completed
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
#                time.sleep(1.)

                try:
                    print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                    pdsub.synchCommand(20,"setTimeout",120.);

                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                except:
# give it one more try
                    print "problem occurred on first readBuffer attempt ... trying once more!"
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
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % archon_version);
    fp.write("%s\n" % archon_revision);    
    fp.close();

# move TS to idle state
                    
    result = tssub.synchCommand(60,"setTSReady");
    rply = result.getResult();

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = monosub.synchCommand(30,"setSlitSize",1,210);
    result = monosub.synchCommand(30,"setSlitSize",2,210);

    result = arcsub.synchCommand(10,"setHeader","TestType","FLAT-DONE")

except Exception, ex:

    print "Exception at %s" % ex

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    result = arcsub.synchCommand(10,"setHeader","TestType","FLAT-ERR")

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f : %s " % (time.time(),exx)

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)

    result = arcsub.synchCommand(10,"setHeader","TestType","FLAT-ERR")

print "FLAT: END"
