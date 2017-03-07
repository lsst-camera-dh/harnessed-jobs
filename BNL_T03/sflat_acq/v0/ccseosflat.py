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

    time.sleep(5.)

    cdir = tsCWD
    
    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)
except:
        print "Exception in initialization"

# make sure it is ready to respond quickly
        arcsub.synchCommand(10,"setParameter","ExpTime","0");
        arcsub.synchCommand(10,"setParameter","WaiTime","200");

# make sure all is quiescent before sending commands to the ammeters
time.sleep(5.0)

print "Setting the current ranges on the Bias and PD devices"
#    biassub.synchCommand(10,"setCurrentRange",0.0002)
pdsub.synchCommand(60,"setCurrentRange",0.00002)

seq = 0  # image pair number in sequence
    
lo_lim = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_LOLIM', default='1.0'))
hi_lim = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_HILIM', default='120.0'))
bcount = float(eolib.getCfgVal(acqcfgfile, 'SFLAT_BCOUNT', default = "5"))
    
#number of PLCs between readings
nplc = 1
    
ccd = CCDID    
print "Working on CCD %s" % ccd

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
    rply = arcsub.synchCommand(60,"exposeAcquireAndSave").getResult()
    rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

try:
    
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
            lohiflux = "L"
            if (target>10000) :
                lohiflux = "H"
#            exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='FLAT', use_nd=False)
    
            imcount = int(tokens[3])
            result = arcsub.synchCommand(10,"setHeader","SequenceNumber",seq)
    
# take bias images
            arcsub.synchCommand(10,"setParameter","ExpTime","0"); 
            result = arcsub.synchCommand(10,"setParameter","Light","0");

            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            result = arcsub.synchCommand(10,"setCCDnum",ccd)
            result = arcsub.synchCommand(10,"setHeader","TestType","SFLAT_500")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

# dispose of first image
            arcsub.synchCommand(10,"setFitsFilename","");
            fitsfilename = arcsub.synchCommand(500,"exposeAcquireAndSave").getResult();
            rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

            time.sleep(0.5)

# now take bias images 
            for i in range(bcount):
                timestamp = time.time()
                fitsfilename = "%s_sflat_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

                print "Ready to take bias image. time = %f" % time.time()
                fitsfilename = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

                print "after click click at %f" % time.time()
                time.sleep(0.2)
# =========================================================================    
# take light exposures
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
            arcsub.synchCommand(10,"setParameter","WaiTime","200");
            result = arcsub.synchCommand(10,"setParameter","Light","1");
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
            print "setting the monochromator wavelength"

            if (wl!=owl) :
                print "Setting monochromator lambda = %8.2f" % wl
                result = monosub.synchCommand(300,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.0)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");
                result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)

# do in-job flux calibration
                arcsub.synchCommand(10,"setParameter","ExpTime","2000");

# dispose of first image
                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                rply = result.getResult();

                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");

                flncal = arcsub.synchCommand(500,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                flux = float(result.getResult());


# scale 
#                flux = flux * 0.50

                print "The flux is determined to be %f" % flux

                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                arcsub.synchCommand(10,"setParameter","WaiTime","200");
                arcsub.synchCommand(10,"setFitsFilename","");
                rply = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                owl = wl

            exptime = target/flux
            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime

# prepare to readout diodes                                                                                  
            if (exptime>0.5) :
                nplc = 1.0
            else :
                nplc = 0.20

            nreads = (exptime+4.0)*60/nplc
            if (nreads > 3000):
                nreads = 3000
                nplc = (exptime+4.0)*60/nreads
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc


            result = arcsub.synchCommand(10,"setHeader","TestType","SFLAT_500")
            result = arcsub.synchCommand(10,"setHeader","ImageType","FLAT")

            print "Throwing away the first image"
#            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
#            arcsub.synchCommand(10,"setFitsFilename","");
#            result = arcsub.synchCommand(500,"exposeAcquireAndSave");
#            reply = result.getResult();
#            result = arcsub.synchCommand(500,"waitForExpoEnd");
#            reply = result.getResult();
##            time.sleep(exptime);

# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*2.00 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            for i in range(imcount):
                print "starting acquisition step for lambda = %8.2f" % wl

                print "call accumBuffer to start PD recording at %f" % time.time()

#                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                arcsub.synchCommand(10,"setParameter Nexpo 1");
                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
                result = arcsub.synchCommand(10,"setParameter","Light","1");
                arcsub.synchCommand(10,"setParameter","WaiTime","200");
                arcsub.synchCommand(10,"setFitsFilename","");
                rply = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();


                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()
# start acquisition

                timestamp = time.time()
                fitsfilename = "%s_sflat_%3.3d_flat_%s%3.3d_${TIMESTAMP}.fits" % (ccd,int(wl),lohiflux,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

# make sure to get some readings before the state of the shutter changes       
                time.sleep(1.5);
    

                print "Ready to take image. time = %f" % time.time()
                fitsfilename = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                rply         = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

                print "after click click at %f" % time.time()
    
                print "done with exposure # %d" % i

                arcsub.synchCommand(10,"setParameter Nexpo 100000");
                arcsub.synchCommand(10,"setParameter","ExpTime","0");
                arcsub.synchCommand(10,"setParameter","WaiTime","200");
                arcsub.synchCommand(10,"setFitsFilename","");
                rply = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

                print "getting photodiode readings"
    
                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (timestamp,seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(5.)
    

# make sure the sample of the photo diode is complete                                                        
#                time.sleep(1.)                                                                              

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)

                try:
                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                except:
# give it one more try                                                                                       
                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()

                print "Finished getting readings at %f" % time.time()
    
                print "adding binary table"
                result = arcsub.synchCommand(500,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)

                print "Finished adding binary table at %f" % time.time()

                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

                print "Finished processing image and adding tables"
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
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % archon_version);
    fp.write("%s\n" % archon_revision);    
    fp.close();
    
# move TS to idle state
    result = tssub.synchCommand(200,"setTSReady");
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

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)

print "SFLAT: END"
