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
    acqname = "PERSISTENCE"

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
    print "attaching Lamp subsystem"
    lampsub = CCS.attachSubsystem("%s/Lamp" % ts );

    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);
    
    cdir = tsCWD
    
    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)

    arcsub.synchCommand(10,"setParameter","Fe55","0")

    print "Setting the current ranges on the Bias and PD devices so they don't overflow when the full power of the lamp is bearing down on the diodes"
#    biassub.synchCommand(10,"setCurrentRange",0.0002)
    pdsub.synchCommand(10,"setCurrentRange",0.0002)

# nominal setup
    result =monosub.synchCommand(60,"setFilter",1); # open
    rply = result.getResult()
    result =monosub.synchCommand(30,"setWave",0.);  # full spectrum blast
    rply = result.getResult()

# wait
    for i in range(10):
        print "doing long wait ... step %d " % i
        time.sleep(60.)

# go through config file looking for  instructions, execute
 
    arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
#number of PLCs between readings
    nplc = 1.0
    
    ccd = CCDID
    print "Working on CCD %s" % ccd
#    seq  = 0
    lseq = 0
    dseq = 0
    bseq = 0

    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'PERSIST_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'PERSIST_HILIM', default='120.0'))


    print "Scanning config file for persist specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    result = arcsub.synchCommand(10,"setCCDnum",ccd)
    
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
    
                result = arcsub.synchCommand(10,"setHeader","TestType",acqname)
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
                for i in range(bcount):
                    timestamp = time.time()
    
                    print "set fits filename"
                    fitsfilename = ""
                    if dowrite==1 :
                        fitsfilename = "%s_persistence_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,bseq)
                    result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
    
                    print "Ready to take bias image. time = %f" % time.time()
                    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                    fitsfilename = result.getResult();
                    print "after click click at %f" % time.time()
                    time.sleep(0.2)
                    bseq = bseq + 1

            if (acqtype==1 or acqtype==2) :
    
    
                print "start image exposure loop"
                lightdark = "undef"
                if (acqtype==1) :
                    result = arcsub.synchCommand(10,"setHeader","ImageType","FLAT")
                    lightdark = "flat"
                    print "Received instruction for doing some Light exposures"
# take light exposures
                    target = float(tokens[2])
                    print "target exposure = %d" % (target);
                    wl = 0.
                    if (len(tokens)>4) :
                        wl = float(tokens[4])
                    exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)
                    arcsub.synchCommand(10,"setParameter","Light","1");
                    imcount = int(tokens[3])

# set the wavelngth
                    if (len(tokens)>4) :
#                    result =monosub.synchCommand(30,"setWaveAndFilter",wl);
                        result =monosub.synchCommand(60,"setWave",wl);
                        rply = result.getResult()
                        time.sleep(4.0)

# publish the state of the system so that the header data will be current
                    print "publishing state"
                    result = tssub.synchCommand(60,"publishState");
                    stt = result.getResult()

                else :
                    lightdark = "dark"
                    result = arcsub.synchCommand(10,"setHeader","ImageType","DARK")
                    print "Received instruction for doing some Dark exposures"
# take exposures
                    arcsub.synchCommand(10,"setParameter","Light","0")
                    exptime = float(tokens[2])
                    imcount = int(tokens[3])

#  ---- the rest is common to light/dark

                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
# prepare to readout diodes
                nreads = exptime*60/nplc + 200
                if (nreads > 3000):
                    nreads = 3000
                    nplc = exptime*60/(nreads-200)
                    print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc
    
                result = arcsub.synchCommand(10,"setHeader","TestType",acqname)

# adjust timeout because we will be waiting for the data to become ready both
# at the accumbuffer stage and the readbuffer stage
                mywait = nplc/60.*nreads*1.10 ;
                print "Setting timeout to %f s" % mywait
                pdsub.synchCommand(1000,"setTimeout",mywait);

                for i in range(imcount):
    
                    print "call accumBuffer to start PD recording at %f" % time.time()
                    pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);
    
                    print "recording should now be in progress and the time is %f" % time.time()
    
# start acquisition
    
                    timestamp = time.time()
    

# ITL-113-10-3XXKhz_persist_dark_001_<timestamp>.fits
                    if (acqtype == 1 ) :
                        iseq = lseq
                    if (acqtype == 2 ) :
                        iseq = dseq
                    fitsfilename = "%s_persistence_%s_%3.3d_${TIMESTAMP}.fits" % (ccd,lightdark,iseq)
                    arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
        
                    print "Ready to take image. time = %f" % time.time()
                    result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                    fitsfilename = result.getResult();
                    print "after click click at %f" % time.time()
        
                    print "done with exposure # %d" % i
                    print "getting photodiode readings at time = %f" % time.time();
    
                    pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),iseq,i+1)
    
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                    print "starting the wait for an accumBuffer done status message at %f" % time.time()
                    tottime = pdresult.get();
    
# make sure the sample of the photo diode is complete
                    time.sleep(5.)
        
                    print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                    result = pdsub.synchCommand(900,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                    print "Finished getting readings at %f" % time.time()

                    if (exptime > 0.0) :
                        result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                    fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

                    if (acqtype == 1 ) :
                        lseq = lseq + 1
                    if (acqtype == 2 ) :
                        dseq = dseq + 1
     
      
# reset timeout to something reasonable for a regular command
                pdsub.synchCommand(1000,"setTimeout",10.);
    
    fpfiles.close();
    fp.close();
    
    fp = open("%s/status.out" % (cdir),"w");
    
    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    
    fp.close();
    
# turn off the lamp
    print "TURNING OFF THE LAMP"
    result = lampsub.synchCommand(100000,"setLampPowerEnable",False);

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

print "%s: END" % acqname
