###############################################################################
# qe
# Acquire qe images for RAFT EO testing at TS8
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

doPD = False
runnum = "no-eTrav"
try:
    runnum = tsCWD.split('/')[len(tsCWD.split('/'))-4]
except:
    pass

print "Run number = %s" % runnum

if (True):
#attach CCS subsystem Devices for scripting
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
    print "attaching Bias subsystem"
    biassub   = CCS.attachSubsystem("%s/Bias" % ts);
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
#    print "attaching PDU subsystem"
#    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "Attaching ts8 subsystem"

    ts8sub  = CCS.attachSubsystem("ts8");

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""


# get the software versions to include in the data products to be persisted in the DB
#    ts_version,ts8_version,ts_revision,ts8_revision = eolib.EOgetCCSVersions(tssub,cdir)

# prepare TS8: make sure temperature and vacuum are OK and load the sequencer
#    eolib.EOSetup(tssub,RAFTID,CCSRAFTTYPE,cdir,sequence_file,vac_outlet,ts8sub)

    result = monosub.synchCommand(20,"openShutter");

# full path causes length problem: /home/ts8prod/lsst/redhat6-x86_64-64bit-gcc44/test/jh_inst/0.3.23/harnessed-jobs-0.3.23/config/BNL/sequencer-ts8-ITL-v4.seq
    acffile = "/home/ts8prod/workdir/sequencer-ts8-ITL-v4.seq"

    print "sequencer file = %s " % acffile
    result = ts8sub.synchCommand(90,"loadSequencer",acffile);


    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'QE_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'QE_HILIM', default='120.0'))
    bcount = int(eolib.getCfgVal(acqcfgfile, 'QE_BCOUNT', default='1'))
    imcount = int(eolib.getCfgVal(acqcfgfile, 'QE_IMCOUNT', default='2'))

    bcount = 1

    seq = 0

#number of PLCs between readings
    nplc = 1.0

#    raft = RAFTID
    raft = CCDID
    print "Working on RAFT %s" % raft

# go through config file looking for 'qe' instructions
    print "Scanning config file for QE specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'lambda')):
            wl = int(tokens[1])
            target = float(tokens[2])
            print "wl = %f" % wl;

            print "setting the monochromator wavelength to %f" % wl

            result = monosub.synchCommand(1000,"setWaveAndFilter",wl);
            rwl = result.getResult()
            time.sleep(10.)
            if (abs(wl-rwl)>1.0) :
                print "ALERT ALERT ALERT MONOCHROMATOR APPEARS NOT TO HAVE REACHED THE DESIRED WAVELENGTH"
                print "request wl = %f" % wl
                print "getwave returned wl = %f" % rwl
                print "SKIPPING THIS WAVELENGTH!"
                continue
            print "publishing state"
            result = tssub.synchCommand(60,"publishState");
            print "The wl retrieved from the monochromator is rwl = %f" % rwl

#
# take bias images
# 

            print "setting location of bias fits directory"
#/<raft ID>/<run ID>/<acquisition type>/<test version>/<activity ID>/S<2-digit location in raft>

            ts8sub.synchCommand(10,"setDefaultImageDirectory","%s/${sensorLoc}" % (cdir));


            ts8sub.synchCommand(10,"setTestType","qe")
            ts8sub.synchCommand(10,"setRaftLoc",str(raft))

# probably not needed any more ... reduce count to 1
            for i in range(1):
                timestamp = time.time()
                print "Ready to take clearing bias image. time = %f" % time.time()
# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
                ts8sub.synchCommand(90,"exposeAcquireAndSave",0,False,False,"${sensorId}_${raftLoc}_${test_type}_${image_type}_%s_${timestamp}.fits" % runnum );

                print "after click click at %f" % time.time()

            time.sleep(3.0)

            for i in range(bcount):
                timestamp = time.time()

                print "Ready to take bias image. time = %f" % time.time()

                ts8sub.synchCommand(10,"setTestType","qe")
                ts8sub.synchCommand(10,"setImageType","bias")
                ts8sub.synchCommand(50,"exposeAcquireAndSave",0,False,False,"${sensorId}_r${raftLoc}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits");

                print "after click click at %f" % time.time()
#                time.sleep(3.0)


# do in-job flux calibration
# #####################################################################################3
# dispose of first image

                testfitsfiles = ts8sub.synchCommand(500,"exposeAcquireAndSave",2000,True,False,"fluxcalib_${sensorId}_${test_type}_${image_type}_${seq_info}_%s_${timestamp}.fits" % runnum).getResult();
                
                time.sleep(2.0)

                testfitsfiles = ts8sub.synchCommand(500,"exposeAcquireAndSave",2000,True,False,"fluxcalib_${sensorId}_${test_type}_${image_type}_${seq_info}_%s_${timestamp}.fits" % runnum).getResult();

                fluxsum = 0.0
                nflux = 0
                for flncal in testfitsfiles:
                    result = ts8sub.synchCommand(10,"getFluxStats",flncal);
                    fluxsum += float(result.getResult());
                    nflux ++;

                flux = fluxsum / nflux;

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

# prepare to readout diodes
            if (exptime>0.5) :
                nplc = 1.0
            else :
                nplc = 0.25


            nreads = (exptime+2.0)*60/nplc
            if (nreads > 3000):
                nreads = 3000
                nplc = (exptime+2.0)*60/nreads
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc


# adjust timeout because we will be waiting for the data to become ready
            mywait = nplc/60.*nreads*2.00 ;
            print "Setting timeout to %f s" % mywait
            pdsub.synchCommand(1000,"setTimeout",mywait);


            result = ts8sub.synchCommand(90,"loadSequencer",acffile);

            for i in range(imcount):
                print "image number = %d" % i

                print "call accumBuffer to start PD recording at %f" % time.time()
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                if (doPD) :
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

# start acquisition
                timestamp = time.time()


# make sure to get some readings before the state of the shutter changes       
                time.sleep(1.0);

                print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())

                ts8sub.synchCommand(10,"setTestType","qe")
                ts8sub.synchCommand(10,"setImageType","qe")

# <CCD id>_<test type>_<image type>_<seq. #>_<run_ID>_<time stamp>.fits
                result = ts8sub.synchCommand(50,"exposeAcquireAndSave",int(exptime*1000),True,False,"${sensorId}_${test_type}_${image_type}_${seq_info}_%s_${timestamp}.fits" % runnum);

                fitsfiles = result.getResult()

                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i
                print "getting photodiode readings at time = %f" % time.time();

                if (doPD) :
                    pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                    print "starting the wait for an accumBuffer done status message at %f" % time.time()
                    tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                    time.sleep(2.)

                    print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)

                    result = pdsub.synchCommand(1000,"readBuffer","/%s/%s" % (cdir,pdfilename),"ts8prod@ts8-raft1");
                    buff = result.getResult()
                    print "Finished getting readings at %f" % time.time()

                    time.sleep(10)

                    for fitsfilename in fitsfiles :
                        print "adding binary table of PD values for %s" % fitsfilename

                        result = ts8sub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),"%s/%s" % (cdir,fitsfilename),"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)


# ------------------- end of imcount loop --------------------------------
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
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.close();

# move TS to idle state
                    
#    result = tssub.synchCommand(200,"setTSReady");
#    rply = result.getResult();

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
try:
    result = ts8sub.synchCommand(10,"setTestType","QE-END")
    print "something"

except Exception, ex:

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)


print "QE!: END"
