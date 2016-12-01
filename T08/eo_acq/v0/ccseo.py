###############################################################################
# 
# Acquire images for RAFT EO testing at TS8
#   
#   Date: 11/29/2016
#   Author: H. Neal
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time
import eolib
import glob

CCS.setThrowExceptions(True);

doPD = False
runnum = "no-eTrav"
try:
    runnum = RUNNUM
except:
    pass

print "Run number = %s" % runnum

if (True):
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


    acqname = jobname.split("_")[0].upper()
    if (acqname == "QE") :
        acqname = "LAMBDA"

    time.sleep(3.)

    cdir = tsCWD

    raft = UNITID


    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""


# get the software versions to include in the data products to be persisted in the DB
    ts_version,ts8_version,ts_revision,ts8_revision = eolib.EOgetTS8CCSVersions(tssub,cdir)


    ccdnames = {}
    ccdmanunames = {}
    try:
        ccdnames["00"] = CCDS00
        ccdmanunames["00"] = CCDMANUS00
        ccdnames["01"] = CCDS01
        ccdmanunames["01"] = CCDMANUS01
        ccdnames["02"] = CCDS02
        ccdmanunames["02"] = CCDMANUS02
    except:
        pass
    try:
        ccdnames["10"] = CCDS10
        ccdmanunames["10"] = CCDMANUS10
        ccdnames["11"] = CCDS11
        ccdmanunames["11"] = CCDMANUS11
        ccdnames["12"] = CCDS12
        ccdmanunames["12"] = CCDMANUS12
    except:
        pass
    try:
        ccdnames["20"] = CCDS20
        ccdmanunames["20"] = CCDMANUS20
        ccdnames["21"] = CCDS21
        ccdmanunames["21"] = CCDMANUS21
        ccdnames["22"] = CCDS22
        ccdmanunames["22"] = CCDMANUS22
    except:
        pass

# prepare TS8: make sure temperature and vacuum are OK and load the sequencer
    rafttype = "ITL"
    eolib.EOTS8Setup(tssub,ts8sub,raft,rafttype,ccdnames,ccdmanunames,cdir,sequence_file,vac_outlet)

    result = monosub.synchCommand(20,"openShutter");


    lo_lim = float(eolib.getCfgVal(acqcfgfile, '%s_LOLIM' % acqname, default='0.025'))
    hi_lim = float(eolib.getCfgVal(acqcfgfile, '%s_HILIM' % acqname, default='600.0'))
    bcount = int(eolib.getCfgVal(acqcfgfile, '%s_BCOUNT' % acqname, default='1'))

    imcount = 0
    if 'FLAT' in acqname :
        imcount = int(eolib.getCfgVal(acqcfgfile, '%s_IMCOUNT' % acqname, default='2'))
    else :
        imcount = int(eolib.getCfgVal(acqcfgfile, '%s_IMCOUNT' % acqname, default='1'))
    wl     = float(eolib.getCfgVal(acqcfgfile, '%s_WL' % acqname, default = "550.0"))

# bias image count
    bcount = 1
# sequence number
    seq = 0
# old wave length setting
    owl = -1.0
# number of PulseLinceCounts between readings
    nplc = 1.0
# exposure time
    exptime = -1
# default file pattern
    def_pat = "${CCDSerialLSST}_${TestType}_${ImageType}_${SequenceInfo}_${RunNumber}_${timestamp}.fits"
    ts8sub.synchCommand(10,"setFitsFileNamePattern",def_pat)
# flat file pattern
# E2V-CCD250-179_flat_0065.07_flat2_20161130064552.fits
    flat_pat = '${CCDSerialLSST}_${TestType}_%07.2f_${ImageType}%d_${SequenceInfo}_${RunNumber}_${timestamp}.fits'
# qe file pattern
# E2V-CCD250-179_lambda_flat_1100_076_20161130124533.fits
    qe_pat = '${CCDSerialLSST}_${TestType}_${ImageType}_%4.4d_${SequenceInfo}_${RunNumber}_${timestamp}.fits'


    print "Working on RAFT %s" % raft

# keep list of produced files
    fpfiles = open("%s/acqfilelist" % cdir,"w");

# count how many instructions there are
    fp = open(acqcfgfile,"r");
    number_instr = 0
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == acqname.lower())):
            number_instr += 1
    fp.close()

# ---- now start --------------
# go through EO test config file looking for instructions
    print "Scanning config file for specifications for %s" % acqname.lower();
    fp = open(acqcfgfile,"r");
    for line in fp:

# split the instruction according to test type
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == acqname.lower())):

            print "==== working on sequence %d  Total# = %d" % (seq,number_instr)

            doXED = False
            doLight = False

            if 'FLAT' in acqname :
# exptime will be set later using the flux calib
                target = float(tokens[1])
# .. indicate that the exposure time must be recalculated
                exptime = -1
                doLight = True
# imcount was already set
            elif 'LAMBDA' in acqname :
                wl = int(tokens[1])
                target = float(tokens[2])
# .. indicate that the exposure time must be recalculated
                exptime = -1
                doLight = True
                print "wl = %f" % wl;
            else
                exptime = float(tokens[1])
                imcount = float(tokens[2])
                if 'PPUMP' in acqname :
                    nshifts  = float(tokens[3])
                else if 'FE55' in acqname :
                    doXED = True
            print "found instructions for exptime = %f and image count = %d" % (exptime,imcount)

# ==================================================
# setup meta data for these exposures
# ==================================================
            print "setting location of fits directory"

            ts8sub.synchCommand(10,"setDefaultImageDirectory","%s/${sensorLoc}" % (cdir));

            ts8sub.synchCommand(10,"setRaftName",str(raft))
            ts8sub.synchCommand(10,"setRunNumber",runnum)

# ==================================================
# take bias images
# ==================================================

# probably not needed any more ... reduce count to 1
            for i in range(1):
                timestamp = time.time()
                print "Ready to take clearing bias image. time = %f" % time.time()
                ts8sub.synchCommand(10,"setTestType",acqname.lower())
                ts8sub.synchCommand(10,"setImageType","biasclear")
                ts8sub.synchCommand(10,"setSeqInfo",seq)
                try:
                    rply = ts8sub.synchCommand(200,"exposeAcquireAndSave",0,False,False).getResult()
                    print "clearing acquisition completed"
                except Exception, ex:
                    print "Proceeding despite error: %s" % str(ex)
                    pass
                print "after click click at %f" % time.time()

            time.sleep(3.0)
# now do the useful bias acquisitions
            num_tries = 0
            max_tries = 3
            while i<bcount:
                try:
                    timestamp = time.time()

                    print "Ready to take bias image. time = %f" % time.time()

                    ts8sub.synchCommand(10,"setTestType",acqname.lower())
                    ts8sub.synchCommand(10,"setImageType","bias")
                    rply = ts8sub.synchCommand(50,"exposeAcquireAndSave",0,False,False).getResult()
                    print "completed bias exposure"
                    i += 1
                    num_tries = 0
                except Exception, ex:
                    num_tries += 1
                    if num_tries < max_tries:
                        print "RETRYING BIAS EXPOSURE - Error was: %s" % ex
                        time.sleep(10.0)
                    else:
                        raise Exception("EXCEEDED MAX RETRIES ON BIAS EXPOSURE: %s" % str(ex))

                print "after click click at %f" % time.time()
#                time.sleep(3.0)


########################## Start of flux calib section #############################
            if (('FLAT' in acqname or 'LAMBDA' in acqname) and wl!=owl):
                                            
                print "Setting monochromator lambda = %8.2f" % wl
                result = monosub.synchCommand(60,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.0)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");


# dispose of first image
                ts8sub.synchCommand(10,"setTestType",acqname.lower())
                ts8sub.synchCommand(10,"setImageType","prefluxcalib")
                ts8sub.synchCommand(10,"setSeqInfo",seq)
                try:
                    testfitsfiles = ts8sub.synchCommand(500,"exposeAcquireAndSave",2000,True,False).getResult();
                except:
                    pass
                time.sleep(2.0)

# now do the useful exposure for the flux calibration
                success = False
                num_tries = 0
                max_tries = 3
                while not success:
                    try:
                        ts8sub.synchCommand(10,"setTestType",acqname.lower())
                        ts8sub.synchCommand(10,"setImageType","fluxcalib")
                        ts8sub.synchCommand(10,"setSeqInfo",seq)

                        testfitsfiles = ts8sub.synchCommand(500,"exposeAcquireAndSave",2000,True,False).getResult();

                        success = True
                    except Exception, ex:
                        num_tries += 1
                        if num_tries > max_tries :
                            raise Exception("EXCEEDED MAXIMUM NUMBER OF RETRIES FOR FLUX CALIB: %s" % str(ex))
                        else:
                            print "RETRYING FLUX CALIB EXPOSURE"
                            time.sleep(10.0)
                print "fitsfiles = "
                print testfitsfiles

                fluxsum = 0.0
                nflux = 0
                for flncal in testfitsfiles:
                    flncalpath = glob.glob("%s/*/%s" % (tsCWD,flncal))[0]
                    print "full flux file path = %s" % flncalpath
                    result = ts8sub.synchCommand(10,"getFluxStats","%s" % flncalpath);
                    fluxsum += float(result.getResult());
                    nflux=nflux+1;

                flux = fluxsum / nflux;

                print "The flux is determined to be %f" % flux

                owl = wl
# ####################################################################################
                print "raw flux value = %f" % flux
                if (flux < 2.0) :
                # must be a test
                    flux = 300.0
                print "SETTING A DEFAULT TEST FLUX OF 300 DUE TO APPARENT NO SENSOR TEST IN PROGRESS"

####################### End of flux calib section ###########################################

# check if exptime needs to be recalculated
            if (exptime < 0.):
                exptime = target/flux

            print "needed exposure time = %f" % exptime
            if (exptime > hi_lim) :
                exptime = hi_lim
            if (exptime < lo_lim) :
                exptime = lo_lim
            print "adjusted exposure time = %f" % exptime

# =========================================
# prepare to readout photodiodes                
# =========================================
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
#temp            pdsub.synchCommand(1000,"setTimeout",mywait);

# =====================================================================================
#       EXPOSE
# =====================================================================================
            num_tries = 0
            max_tries = 3
            imdone=0
            print "starting exposure sequence %d for %d images" % (seq,imcount)
            while imdone<imcount :
                try:
                    print "images completed number = %d" % imdone

                    if (doPD) :
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

                    timestamp = time.time()

# make sure to get some readings before the state of the shutter changes       
                    time.sleep(1.0);

                    print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())
                
                    ts8sub.synchCommand(10,"setTestType",acqname.lower())
                    ts8sub.synchCommand(10,"setImageType",acqname.lower())
                    ts8sub.synchCommand(10,"setSeqInfo",seq)
#                        ts8sub.synchCommand(10,"setSeqInfo","%s_%07.2f" % (str(seq),exptime))

                    if 'FLAT' in acqname :
                        ts8sub.synchCommand(10,"setFitsFileNamePattern",flat_pat % (exptime,imdone+1))
                    if 'LAMBDA' in acqname :
                        ts8sub.synchCommand(10,"setFitsFileNamePattern",qe_pat % int(wl))

                    fitsfiles = ts8sub.synchCommand(700,"exposeAcquireAndSave",int(exptime*1000),doLight,doXED).getResult();
                    ts8sub.synchCommand(10,"setFitsFileNamePattern",def_pat)

                    print "after click click at %f" % time.time()
                    print "done with exposure # %d" % imdone

# =======================================
#  retrieve the photodiode readings
# =======================================

                    if (doPD) :
                        print "getting photodiode readings at time = %f" % time.time();

                        pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)

                        print "starting the wait for an accumBuffer done status message at %f" % time.time()
                        tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                        time.sleep(2.)

                        print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)

#                result = pdsub.synchCommand(1000,"readBuffer","/tmp/%s" % pdfilename);
                        result = pdsub.synchCommand(1000,"readBuffer","/%s/%s" % (cdir,pdfilename),"ts8prod@ts8-raft1");
                        buff = result.getResult()
                        print "Finished getting readings at %f" % time.time()

                        time.sleep(5.0)

                        for fitsfilename in fitsfiles :
                            print "adding binary table of PD values for %s" % fitsfilename
                            result = ts8sub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),"%s/%s" % (cdir,fitsfilename),"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                            fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))
# ===================== end of PD value retrieval and end of exposure section ======================
                    print "successful exposure .... incrementing images completed count"
                    imdone = imdone + 1
                    num_tries = 0
                except Exception, ex:
                    num_tries += 1
                    if num_tries > max_tries :
                        raise Exception('TOO MANY RETRIES! %s' % str(ex))
                    else :
                        print "something went wrong during the exposure ... RETRYING: %s" % str(ex)
                        rply = pdsub.synchCommand(10,"softReset").getResult()
                        time.sleep(10.0)
                print "checking ... imdone = %d" % imdone
            print "incrementing sequence number"
            seq += 1
# ------------------- end of imcount loop --------------------------------

# reset timeout to something reasonable for a regular command
#            pdsub.synchCommand(1000,"setTimeout",10.);


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
    result = ts8sub.synchCommand(10,"setTestType","%s-END" % acqname)
    print "something"

except Exception, ex:

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    rply = pdsub.synchCommand(10,"softReset").getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, exx:

    print "ScriptingTimeoutException at %f " % time.time()

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    rply = pdsub.synchCommand(10,"softReset").getResult()

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % exx)


print "%s: END" % acqname
