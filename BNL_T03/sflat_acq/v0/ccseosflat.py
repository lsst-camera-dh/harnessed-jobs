###############################################################################
# sflat
# Acquire sflat images
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
    reply = result.getResult();
    print "Applying configuration"
    result = arcsub.synchCommand(25,"applyConfig");
    reply = result.getResult();
    print "Powering on the CCD"
    result = arcsub.synchCommand(30,"powerOnCCD");
    reply = result.getResult();
    time.sleep(60.);
    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");
    
# the first image is usually bad so throw it away
    print "Throwing away the first image"
    arcsub.synchCommand(10,"setFitsFilename","");
    result = arcsub.synchCommand(200,"exposeAcquireAndSave");
    reply = result.getResult();

    print "Setting the current ranges on the Bias and PD devices"
#    biassub.synchCommand(10,"setCurrentRange",0.0002)
    pdsub.synchCommand(10,"setCurrentRange",0.00002)

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

# ramp the bias
    print "go teststand go"
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();
    
    seq = 0  # image pair number in sequence
    
# get the glowing vacuum gauge off
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
    rply = result.getResult();

    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_HILIM', default='120.0'))
    bcount = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_BCOUNT', default = "5"))
    
#number of PLCs between readings
    nplc = 1
    
    ccd = CCDID    
    print "Working on CCD %s" % ccd

 clear the buffers                                                                                          
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

    
# go through config file looking for 'sflat' instructions
    print "Scanning config file for SFLAT specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");
    
    owl = 0.
    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'sflat')):
            wl = int(tokens[1])
            target = int(tokens[2])
#            exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)
    
            imcount = int(tokens[3])
    
# take bias images
# 2sec for the bias
            arcsub.synchCommand(10,"setParameter","ExpTime","0"); 
            result = arcsub.synchCommand(10,"setParameter","Light","0");

            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "set filter position"
            result = monosub.synchCommand(60,"setFilter",1); # open position
            reply = result.getResult();

            result = arcsub.synchCommand(10,"setHeader","TestType","FLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
            for i in range(bcount):
                timestamp = time.time()
                fitsfilename = "%s_sflat_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)
# =========================================================================    
# take light exposures
            result = arcsub.synchCommand(10,"setParameter","Light","1");
#            result = arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
            print "setting the monochromator wavelength"

            if (wl!=owl) :
                try:
                    print "Setting monochromator lambda = %8.2f" % wl
                    try:
                        result = monosub.synchCommand(30,"setWaveAndFilter",wl);
# result = monosub.synchCommand(200,"setWave",wl);
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
                            print "here we go ... its gotta work this time .... right?"
                            result = monosub.synchCommand(300,"setWave",wl);
                            rply = result.getResult()
                            print "we survived a near crash"
                            time.sleep(4.0)
                    result = monosub.synchCommand(300,"getWave");
                    rwl = result.getResult()
                except ScriptingTimeoutException, ex:
                    print "Failed to get monochromator to respond. Try one more time"
                    try:
                        time.sleep(30.)
                        result = monosub.synchCommand(300,"getWave");
                        rwl = result.getResult()
                    except ScriptingTimeoutException, ex:
                        print "Failed to get monochromator to respond. Skipping to the next step."
                        continue

                print "publishing state"
                result = tssub.synchCommand(60,"publishState");

# do in-job flux calibration
                arcsub.synchCommand(10,"setParameter","ExpTime","2000");

# dispose of first image
                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                rply = result.getResult();

                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");

                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                flncal = result.getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                flux = float(result.getResult());

# cleanup
#            os.rm(flncal)
# scale 
                flux = flux * 0.50

                print "The flux is determined to be %f" % flux

                owl = wl

            exptime = target/flux
            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            result = arcsub.synchCommand(10,"setHeader","TestType","SFLAT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","SFLAT")

            print "Throwing away the first image"
            arcsub.synchCommand(10,"setFitsFilename","");
            result = arcsub.synchCommand(500,"exposeAcquireAndSave");
            reply = result.getResult();
            result = arcsub.synchCommand(500,"waitForExpoEnd");
            reply = result.getResult();
#            time.sleep(exptime);

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
                fitsfilename = "%s_sflat_%3.3d_%3.3d_flat%d_${TIMESTAMP}.fits" % (ccd,int(wl),seq,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.2);
    
    
                print "Ready to take image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
    
                print "done with exposure # %d" % i
                print "getting photodiode readings"
    
                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (timestamp,seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
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
# ---------------- end of loop imcount -------------------------------
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

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)

print "SFLAT: END"
