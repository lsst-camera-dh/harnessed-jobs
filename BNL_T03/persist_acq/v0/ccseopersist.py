###############################################################################
# persist_acq
# - test for persistent images 
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

try:
    acqname = "persist"

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
#    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");

# the first image is usually bad so throw it away
    print "Throwing away the first image"
    arcsub.synchCommand(10,"setFitsFilename","");
    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
    reply = result.getResult();

    
# move to TS acquisition state
    print "setting acquisition state"
    result = tssub.synchCommand(10,"setTSTEST");
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
    print "go teststand go"
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

# get the glowing vacuum gauge off
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
    rply = result.getResult();

# go through config file looking for  instructions, execute
 
    arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
#number of PLCs between readings
    nplc = 1.0
    
    ccd = CCDID
    print "Working on CCD %s" % ccd

    seq = 0
    
# first start with a 10 min 

    print "Scanning config file for persist specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");
    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'persist')):
            acqtype = int(tokens[1])
            print "line = %s" % line
            print "number of tokens = %d" % len(tokens)
            if (acqtype==0) :
                bcount = int(tokens[2])
                dowrite = 1
                if len(tokens)>3 :
                    dowrite = int(tokens[3])

                print "start bias image exposure loop"
                arcsub.synchCommand(10,"setParameter","ExpTime","0");
    
                for i in range(bcount):
                    timestamp = time.time()
    
                    print "set fits filename"
                    fitsfilename = ""
                    if dowrite==1 :
                        fitsfilename = "%s_%s_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,acqname,seq)
                    result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                    result = arcsub.synchCommand(10,"setHeader","TestType",acqname)
                    result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
    
                    print "Ready to take bias image. time = %f" % time.time()
                    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                    fitsfilename = result.getResult();
                    print "after click click at %f" % time.time()
                    time.sleep(0.2)

            if (acqtype==1 or acqtype==2) :
    
    
                print "start image exposure loop"
                lightdark = "undef"
                if (acqtype==1) :
                    lightdark = "light"
                    print "Received instruction for doing some Light exposures"
# take light exposures
                    target = float(tokens[2])
                    print "target exposure = %d" % (target);
                    exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)
                    arcsub.synchCommand(10,"setParameter","Light","1");
                    imcount = int(tokens[3])

# set the wavelngth
                    wl = 0.
                    if (len(tokens)>4) :
                        wl = float(tokens[4])
                    result =monosub.synchCommand(30,"setWaveAndFilter",wl);
#    result = monosub.synchCommand(60,"setWave",wl);
                    rply = result.getResult()
                    time.sleep(4.0)

# publish the state of the system so that the header data will be current
                    print "publishing state"
                    result = tssub.synchCommand(60,"publishstate");
                    stt = result.getResult()

                else :
                    lightdark = "dark"
                    print "Received instruction for doing some Dark exposures"
# take exposures
                    arcsub.synchCommand(10,"setParameter","Light","0")
                    exptime = float(tokens[2])
                    imcount = int(tokens[3])

                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
# prepare to readout diodes
                nreads = exptime*60/nplc + 200
                if (nreads > 3000):
                    nreads = 3000
                    nplc = exptime*60/(nreads-200)
                    print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc
    
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
    

                    fitsfilename = "%s_%s_%s_%d_${TIMESTAMP}.fits" % (ccd,acqname,lightdark,i+1)
                    arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                    result = arcsub.synchCommand(10,"setHeader","TestType",acqname)
                    result = arcsub.synchCommand(10,"setHeader","ImageType",acqname)
        
                    print "Ready to take image. time = %f" % time.time()
                    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
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
                    result = pdsub.synchCommand(900,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                    print "Finished getting readings at %f" % time.time()
    
# reset timeout to something reasonable for a regular command
                    pdsub.synchCommand(1000,"setTimeout",10.);
    
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
                        
    tssub.synchCommand(10,"setTSReady");

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

except Exception, ex:                                                     


    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "%s: END" % acqname
