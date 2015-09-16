###############################################################################
# ppump
#    script for doing pocket pumping acq
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
    
    cdir = tsCWD
    
    time.sleep(3.)

# clear header setting
    result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",0.0)

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,CCSCCDTYPE,acffile,vac_outlet,arcsub,biassub,pdsub,pdusub)

    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","Fe55","0");
    
    print "Setting the current ranges on the Bias and PD devices"
#    biassub.synchCommand(10,"setCurrentRange",0.0002)
    pdsub.synchCommand(10,"setCurrentRange",0.000002)

    wl     = float(eolib.getCfgVal(acqcfgfile, 'PPUMP_WL', default = "550.0"))
    pcount = float(eolib.getCfgVal(acqcfgfile, 'PPUMP_BCOUNT', default = "25"))
    imcount = 2
    
#number of PLCs between readings
    nplc = 1
    
    seq = 0  # image pair number in sequence
    
    monosub.synchCommand(30,"setFilter",1);
    
# go through config file looking for 'ppump' instructions, take the flats
    print "Scanning config file for PPUMP specifications";
    ccd = CCDID
    
    print "Working on CCD %s" % ccd

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

    
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");
    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'ppump')):
    
            exptime = float(tokens[1])
            imcount = float(tokens[2])
            nshifts  = float(tokens[3])

            result = arcsub.synchCommand(10,"setHeader","SequenceNumber",seq)
    
            print "starting acquisition step for lambda = %8.2f with exptime %8.2f s" % (wl, exptime)
    
            print "setup for dark exposure"
            arcsub.synchCommand(10,"setParameter","Light","0");
            print "set number of pocket pumps to %d" % nshifts
            arcsub.synchCommand(10,"setParameter","Npump",str(nshifts));
            print "set pocket depth"
            arcsub.synchCommand(10,"setParameter","Pdepth","1");
    
# pump with some darks then do a light exposure
            print "take some bias images with exptime = 0"
            arcsub.synchCommand(10,"setParameter","ExpTime","0"); 
            arcsub.synchCommand(10,"setParameter","Light","0");

            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            result = arcsub.synchCommand(10,"setCCDnum",ccd)
            result = arcsub.synchCommand(10,"setHeader","TestType","TRAP")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
            for i in range(pcount):
# start acquisition
                timestamp = time.time()
                fitsfilename = "%s_trap_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
    
                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)

# take light exposures
            arcsub.synchCommand(10,"setParameter","Light","1");
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime)));
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "setting the monochromator wavelength"
#            if (exptime > lo_lim):
            result = monosub.synchCommand(30,"setWaveAndFilter",wl);
            rply = result.getResult()
            time.sleep(4.)
            result = monosub.synchCommand(30,"getWave");
            rwl = result.getResult()
            print "publishing state"
            result = tssub.synchCommand(60,"publishState");
            result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)
    
# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            result = arcsub.synchCommand(10,"setHeader","TestType","TRAP")
            result = arcsub.synchCommand(10,"setHeader","ImageType","PPUMP")
            for i in range(imcount):
#                print "Throwing away the first image"
#                arcsub.synchCommand(10,"setFitsFilename","");
#                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
#                reply = result.getResult();


# adjust timeout because we will be waiting for the data to become ready
                mywait = nplc/60.*nreads*1.10 ;
                print "Setting timeout to %f s" % mywait
                pdsub.synchCommand(1000,"setTimeout",mywait);

                print "call accumBuffer to start PD recording at %f" % time.time()
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition
                timestamp = time.time()
    
                fitsfilename = "%s_trap_ppump_%3.3d_%3.3d_${TIMESTAMP}.fits" % (ccd,seq,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.2);
    
                print "Ready to take image. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
    
                print "done with exposure # %d" % i
                print "getting photodiode readings"
    
                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (timestamp,seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(1.)
    
                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()


                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))
    
            seq = seq + 1
    
    fpfiles.close();
    fp.close();
    
    fp = open("%s/status.out" % (cdir),"w");
    
    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    
    fp.close();
    
# move TS to ready state
    result = tssub.synchCommand(60,"setTSReady");
    reply = result.getResult();
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

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
print "PPUMP: END"
