###############################################################################
# fe55
# Acquire fe55 images for RAFT EO testing at TS8
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib
import string

CCS.setThrowExceptions(True);

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


    lo_lim = float(eolib.getCfgVal(acqcfgfile, 'FE55_LOLIM', default='1.0'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, 'FE55_HILIM', default='120.0'))
    bcount = int(eolib.getCfgVal(acqcfgfile, 'FE55_BCOUNT', default='1'))
    imcount = int(eolib.getCfgVal(acqcfgfile, 'FE55_IMCOUNT', default='1'))

    bcount = 1

    seq = 0

#number of PLCs between readings
    nplc = 1.0

#    raft = RAFTID
    raft = CCDID
    print "Working on RAFT %s" % raft

# go through config file looking for 'fe55' instructions
    print "Scanning config file for FE55 specifications";
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'fe55')):
            exptime  = float(tokens[1])
            imcount = int(tokens[2])

#
# take bias images
# 


            print "setting location of bias fits directory"
            ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));


            ts8sub.synchCommand(10,"setTestType","FE55")
            ts8sub.synchCommand(10,"setRaftLoc",str(raft))

# probably not needed any more ... reduce count to 1
            for i in range(1):
                timestamp = time.time()
                print "Ready to take clearing bias image. time = %f" % time.time()
                ts8sub.synchCommand(90,"exposeAcquireAndSave",0,False,False,"tst25-${sensorLoc}_r${raftLoc}_${test_type}_${image_type}.fits");

                print "after click click at %f" % time.time()

            time.sleep(3.0)

            for i in range(bcount):
                timestamp = time.time()

                print "Ready to take bias image. time = %f" % time.time()

                ts8sub.synchCommand(10,"setTestType","FE55")
                ts8sub.synchCommand(10,"setImageType","BIAS")
                ts8sub.synchCommand(50,"exposeAcquireAndSave",0,False,False,"s${sensorLoc}_r${raftLoc}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits");

                print "after click click at %f" % time.time()
#                time.sleep(3.0)



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

                ts8sub.synchCommand(10,"setTestType","FE55")
                ts8sub.synchCommand(10,"setImageType","FE55")
                result = ts8sub.synchCommand(50,"exposeAcquireAndSave",int(exptime*1000),False,True,"s${sensorLoc}_r${raftLoc}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits");
                fitsfiles = result.getResult()

                print "after click click at %f" % time.time()

                print "done with exposure # %d" % i
                print "getting photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(2.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)

#                result = pdsub.synchCommand(1000,"readBuffer","/tmp/%s" % pdfilename);
                result = pdsub.synchCommand(1000,"readBuffer","/%s/%s" % (cdir,pdfilename),"ts8prod@ts8-raft1");
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()

#                subprocess.Popen(["scp ts8prod@ts8-1","/tmp/%s" % pdfilename,cdir])
                for ii in ["s00","s01","s02","s10","s11","s12","s20","s21","s22"] :
                    fitsfilename = string.replace(fitsfiles, '${sensorLoc}', ii)
                    result = ts8sub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
#                fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))

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
    result = ts8sub.synchCommand(10,"setTestType","FE55-END")
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


print "FE55: END"
