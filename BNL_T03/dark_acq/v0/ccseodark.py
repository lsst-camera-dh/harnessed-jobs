###############################################################################
# dark
# Acquire dark image pairs
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

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)

    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","Fe55","0");

# wait until its dark .... very dark
    time.sleep(30.)

# go through config file looking for 'dark' instructions, take the darks
    
    arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
#number of PLCs between readings
    nplc = 1.0
    
    ccd = CCDID
    print "Working on CCD %s" % ccd

    seq = 0

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


    
    print "Scanning config file for DARK specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    result = arcsub.synchCommand(10,"setFetch_timeout",5000000)

    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'dark')):
            exptime = float(tokens[1])
            imcount = int(tokens[2])

    
            print "start bias image exposure loop"
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
#            arcsub.synchCommand(10,"setAndApplyParam","ExpTime","0");

            result = arcsub.synchCommand(10,"setCCDnum",ccd)

            print "Tossing an image"
            result = arcsub.synchCommand(10,"setFitsFilename","")
            result = arcsub.synchCommand(900,"exposeAcquireAndSave");
            fitsfilename = result.getResult();
            result = arcsub.synchCommand(900,"waitForExpoEnd");
            rply = result.getResult();

            print "moving on to bias images"

            bcount = 3
            for i in range(bcount):
                timestamp = time.time()

                print "set fits filename"
                fitsfilename = "%s_dark_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                result = arcsub.synchCommand(10,"setHeader","TestType","DARK")
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                result = arcsub.synchCommand(500,"waitForExpoEnd");
                rply = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)


            print "start dark image exposure loop"

            print "publishing state"
            result = tssub.synchCommand(60,"publishState");

# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc


            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
            print "Tossing an image before taking a dark frame"
            result = arcsub.synchCommand(10,"setFitsFilename","")
            result = arcsub.synchCommand(900,"exposeAcquireAndSave");
            fitsfilename = result.getResult();
            result = arcsub.synchCommand(900,"waitForExpoEnd");
            rply = result.getResult();


            for i in range(imcount):


# adjust timeout because we will be waiting for the data to become ready both
# at the accumbuffer stage and the readbuffer stage
                mywait = nplc/60.*nreads*1.10 ;
                print "Setting timeout to %f s" % mywait
                pdsub.synchCommand(1000,"setTimeout",mywait);

                print "call accumBuffer to start PD recording at %f" % time.time()
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition

                timestamp = time.time()

                fitsfilename = "%s_dark_dark_%d_${TIMESTAMP}.fits" % (ccd,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                result = arcsub.synchCommand(10,"setHeader","TestType","DARK")
                result = arcsub.synchCommand(10,"setHeader","ImageType","DARK")
#                result = arcsub.synchCommand(10,"setFetch_timeout",int(int(mywait)*1000))

                print "Ready to take image. time = %f" % time.time()
                result = arcsub.synchCommand(10000,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
    
                print "done with exposure # %d" % i
                print "getting photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)

# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(5.)
    
                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(1200,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()

# reset timeout to something reasonable for a regular command
                pdsub.synchCommand(1000,"setTimeout",10.);

                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

# ====================== clear the sensor by taking a bias image =================
                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                fitsfilename = "%s_dark_biasclear_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                result = arcsub.synchCommand(10,"setHeader","TestType","DARK")
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "finished with bias clear %f" % time.time()
 
  
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

    result = arcsub.synchCommand(10,"setHeader","TestType","DARK-DONE")
    
# move TS to idle state
                        
    tssub.synchCommand(10,"setTSReady");

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

    result = arcsub.synchCommand(10,"setHeader","TestType","DARK-ERR")

print "DARK: END"
