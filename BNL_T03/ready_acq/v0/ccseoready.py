###############################################################################
# ready_acq
# test the test stand for readiness
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
    biassub = CCS.attachSubsystem("%s/Bias" % ts);
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);
#    print "attaching XED subsystem"
#    xedsub   = CCS.attachSubsystem("%s/Fe55" % ts);

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    eolib.EOSetup(tssub,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub,"setTSWarm","setTSWarm")


    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","Fe55","0");


#    print "Images will now automatically display in the DS9 window"
#    arcsub.synchCommand(10,"setSendImagesToDS9",True);

    print "Setting the current ranges on the Bias and PD devices"
    biassub.synchCommand(10,"setCurrentRange",0.0002)
    pdsub.synchCommand(10,"setCurrentRange",0.0002)

    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'LAMBDA_HILIM', default='120.0'))
#    bcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_BCOUNT', default='1'))
    bcount = 3
    imcount = int(eolib.getCfgVal(acqcfgfile, 'LAMBDA_IMCOUNT', default='1'))
    imcount = 1

    seq = 0

#number of PLCs between readings
    nplc = 1

    ccd = CCDID
    print "Working on CCD %s" % ccd

    print "set filter position"
    monosub.synchCommand(30,"setFilter",1); # open position

# go through config file looking for 'qe' instructions
    print "Scanning config file for LAMBDA specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    print "Scan at a low and a high wavelength to test monochromator and filter wheel"
    for ii in range(2) :
# use a target signal instead
#            target = float(wl)
#            print "target wl = %f" % target;

#            exptime = eolib.expCheck(calfile, labname, target, wl, hi_lim, lo_lim, test='LAMBDA', use_nd=False)
#            exptime = 10.

# take bias images

            arcsub.synchCommand(10,"setParameter","ExpTime","0"); 
            arcsub.synchCommand(10,"setParameter","Light","0");

            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            result = arcsub.synchCommand(10,"setHeader","TestType","READY")
            result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")
            for i in range(bcount):
                timestamp = time.time()
#                fitsfilename = "%s_lambda_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,seq)
                arcsub.synchCommand(10,"setFitsFilename","");

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
#                result = arcsub.synchCommand(500,"waitForExpoEnd");
#                rply = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)

    time.sleep(4.)
################################## Fe55  ################################3
    for iexp in range(1) :
            arcsub.synchCommand(10,"setParameter","Light","0");
            arcsub.synchCommand(10,"setParameter","Fe55","1");

            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            exptime = 10.0
            print "exposure time = %f" % exptime
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

            result = arcsub.synchCommand(10,"setHeader","SequenceNumber",seq)


# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            result = arcsub.synchCommand(10,"setHeader","TestType","READYFe55")
            result = arcsub.synchCommand(10,"setHeader","ImageType","READYFe55")


# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*1.10 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            for i in range(imcount):
# extend the Fe55 arm
#                print "extend the Fe55 arm"
#                xedsub.synchCommand(30,"extendFe55");

                print "Starting Photo Diode recording at %f" % time.time()
                print "You should see digits changing on the PD device"
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition
                timestamp = time.time()
                fitsfilename = "%s_fe55_%d_${TIMESTAMP}.fits" % (ccd,i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.2);
 

                print "Taking an image now. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "Done taking image at %f" % time.time()

# retract the Fe55 arm
#                xedsub.synchCommand(30,"retractFe55");

                print "done with exposure # %d" % i
                print "retrieving photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(10.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()


                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)

                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

# reset timeout to something reasonable for a regular command
            pdsub.synchCommand(1000,"setTimeout",10.);
            seq = seq + 1

    time.sleep(4.)
############################## LIGHT ###################################3
    arcsub.synchCommand(10,"setParameter","Fe55","0");
    target = 1000.
    for wl in [450.,823.] :
# take light exposures
            arcsub.synchCommand(10,"setParameter","Light","1");
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            do_in_job_flux = false
# do in-job flux cal
            if (do_in_job_flux) :
                arcsub.synchCommand(10,"setParameter","ExpTime","2000");

                arcsub.synchCommand(10,"setFitsFilename","");
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                rply = result.getResult();
                arcsub.synchCommand(10,"setFitsFilename","fluxcalimage-${TIMESTAMP}");

                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                flncal = result.getResult();
                result = arcsub.synchCommand(10,"getFluxStats",flncal);
                flux = float(result.getResult());

                flux = flux * 0.50

                exptime = target/flux
            else :
# for now we have decided to use a fixed time
                exptime = 4.0

            print "exposure time = %f" % exptime
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# prepare to readout diodes
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            result = arcsub.synchCommand(10,"setHeader","TestType","READYLIGHT")
            result = arcsub.synchCommand(10,"setHeader","ImageType","READYLIGHT")

            print "throw away first image after all parameters set"
            arcsub.synchCommand(10,"setFitsFilename","");
            result = arcsub.synchCommand(500,"exposeAcquireAndSave");
            flnthrow = result.getResult();

# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*1.10 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);

            for i in range(imcount):
                print "starting acquisition step for lambda = %8.2f" % wl

                print "Setting the monochrmator wavelength and filter"
                print "You should HEAR some movement"
                result = monosub.synchCommand(90,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");

                print "getting filter wheel setting"
                result = monosub.synchCommand(60,"getFilter");
                ifl = result.getResult()
                print "The wavelength is at %f and the filter wheel is at %f " % (rwl,ifl)
                time.sleep(4.);
                

                print "Starting Photo Diode recording at %f" % time.time()
                print "You should see digits changing on the PD device"
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()

# start acquisition
                timestamp = time.time()
                fitsfilename = "%s_lambda_%3.3d_%d_${TIMESTAMP}.fits" % (ccd,int(wl),i+1)
                arcsub.synchCommand(10,"setFitsFilename",fitsfilename);

# make sure to get some readings before the state of the shutter changes       
                time.sleep(0.2);
 

                print "Taking an image now. time = %f" % time.time()
                result = arcsub.synchCommand(500,"exposeAcquireAndSave");
                fitsfilename = result.getResult();
                print "Done taking image at %f" % time.time()

                print "done with exposure # %d" % i
                print "retrieving photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(10.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()


                result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)

                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

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

# move TS to ready state                    
    tssub.synchCommand(60,"setTSReady");

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");
    arcsub.synchCommand(10,"setParameter","Fe55","0");

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    result = arcsub.synchCommand(10,"setHeader","TestType","READY-DONE")

    print "            TEST ACQUISITIONS COMPLETED"

except Exception, ex:
    arcsub.synchCommand(10,"setParameter","Fe55","0");

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    result = arcsub.synchCommand(10,"setHeader","TestType","READY-Err")

except ScriptingTimeoutException, ex:
    arcsub.synchCommand(10,"setParameter","Fe55","0");

    raise Exception("There was an ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    result = arcsub.synchCommand(10,"setHeader","TestType","READY-Err")

print "TS3_ready: COMPLETED"
