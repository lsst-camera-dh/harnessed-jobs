###############################################################################
# fe55
# Acquire fe55 image pairs
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
#    print "attaching XED subsystem"
#    xedsub   = CCS.attachSubsystem("%s/Fe55" % ts);
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

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

# move TS to ready state
    result = tssub.synchCommand(60,"setTSReady");
    reply = result.getResult();
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

    print "test stand in ready state, now the controller will be configured. time = %f" % time.time()

    print "Loading configuration file into the Archon controller"
    result = arcsub.synchCommand(20,"setConfigFromFile",acffile);
#    result = arcsub.synchCommand(20,"setConfigFromFile","/home/ts3prod/prod/acfs/bnl_STA_20150730_Fe55.acf");
    reply = result.getResult();
    print "Applying configuration"
    result = arcsub.synchCommand(25,"applyConfig");
    reply = result.getResult();
    print "Powering on the CCD"
    result = arcsub.synchCommand(30,"powerOnCCD");
    reply = result.getResult();
    time.sleep(60.);
    print "set controller parameters for an exposure with the shutter closed"
    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");
    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","Fe55","0");

#    arcsub.synchCommand(10,"setDefaultCCDTypeName","BNLITL");

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");

    print "set filter wheel to position 1"
    monosub.synchCommand(30,"setFilter",1); # open position
    
    # move to TS acquisition state
    print "setting acquisition state"
    result = tssub.synchCommand(60,"setTSTEST");
    rply = result.getResult();
    
# get the glowing vacuum gauge off
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
    rply = result.getResult();

    #check state of ts devices
    print "wait for ts state to become ready";
    tsstate = 0
    starttim = time.time()
    while True:
        print "checking for test stand ready to start acq";
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
    print "go teststand go"
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();
    
    print "Now collect some parameters from the config file"
    bcount = float(eolib.getCfgVal(acqcfgfile, 'FE55_BCOUNT', default = "2"))
    dcount = float(eolib.getCfgVal(acqcfgfile, 'FE55_DCOUNT', default = "2"))

    seq = 0

#number of PLCs between readings
    nplc = 1

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

# go through config file looking for 'fe55' instructions, take the fe55s
    print "Scanning config file for fe55 specifications";
    
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");
    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'fe55')):
            exptime  = float(tokens[1])
            imcount = int(tokens[2])
    
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
# take bias images
            print "set controller for bias exposure"
            arcsub.synchCommand(10,"setParameter","Fe55","0");
            arcsub.synchCommand(10,"setParameter","Light","0");
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
 
            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "start bias exposure loop"

            for i in range(bcount):
                timestamp = time.time()

                print "set fits filename"
                fitsfilename = "%s_fe55_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,i)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                result = arcsub.synchCommand(10,"setHeader","TestType","FE55")
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(20,"exposeAcquireAndSave");
                print "wait"
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)

            print "start fe55 exposures"
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            icount = 0
            for itype in range(2):
                if (itype==0) : 
                    itypename = "dark"
                    icount = dcount
                    arcsub.synchCommand(10,"setParameter","Fe55","0");
                if (itype==1) :
                    itypename = "fe55"
                    icount = imcount
                    arcsub.synchCommand(10,"setParameter","Fe55","1");

                for i in range(icount):
                    print "Throwing away the first image"
                    arcsub.synchCommand(10,"setFitsFilename","");
                    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                    reply = result.getResult();


# prepare to readout diodes                                                                              
# adjust timeout because we will be waiting for the data to become ready
                    mywait = nplc/60.*nreads*1.10 ;
                    print "Setting timeout to %f s" % mywait
                    pdsub.synchCommand(1000,"setTimeout",mywait);

                    pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);
#                pdresult =  pdsub.synchCommand(10,"accumBuffer",int(nreads),float(nplc),False);
                    print "recording should now be in progress and the time is %f" % time.time()
# start acquisition

                    timestamp = time.time()
    
# make sure to get some readings before the state of the shutter changes       
                    time.sleep(0.2);

# start acquisition
                    fitsfilename = "%s_fe55_%s_%3.3d_${TIMESTAMP}.fits" % (ccd,itypename,i+1)
                    result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                    result = arcsub.synchCommand(10,"setHeader","TestType","FE55")
                    result = arcsub.synchCommand(10,"setHeader","ImageType","FE55")
    
                    print "Ready to take image. time = %f" % time.time()

# extend the Fe55 arm
#                print "extend the Fe55 arm"
#                xedsub.synchCommand(30,"extendFe55");
    

                    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                    fitsfilename = result.getResult();
                    result = arcsub.synchCommand(500,"waitForExpoEnd");
                    rply = result.getResult();

# retract the Fe55 arm
#                xedsub.synchCommand(30,"retractFe55");
    
                    print "after click click at %f" % time.time()

                    print "done with exposure # %d" % i
                    print "getting photodiode readings at time = %f" % time.time();
    
                    pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (timestamp,seq,i+1)
                    print "starting the wait for an accumBuffer done status message at %f" % time.time()
                    tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                    time.sleep(5.)

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
    
# move TS to idle state
    tssub.synchCommand(60,"setTSReady");

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    time.sleep(5.)

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    arcsub.synchCommand(10,"setParameter","Fe55","0");

    result = arcsub.synchCommand(10,"setHeader","TestType","FE55-DONE")

except Exception, ex:                                                     

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");
    
    arcsub.synchCommand(10,"setParameter","Fe55","0");

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    result = arcsub.synchCommand(10,"setHeader","TestType","FE55-ERR")

#except ScriptingTimeoutException, ex:                                                     

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");
    
#    arcsub.synchCommand(10,"setParameter","Fe55","0");

#    raise Exception("There was an ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "FE55: END"
