###############################################################################
# preflight_acq
# test the test stand for readiness
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);


#attach CCS subsystem Devices for scripting
print "Attaching teststand subsystems"
tssub  = CCS.attachSubsystem("%s" % ts);
print "attaching PD subsystem"
pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
print "attaching Mono subsystem"
monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
print "attaching PDU subsystem"
pdusub = CCS.attachSubsystem("%s/PDU" % ts );
print "Attaching teststand 8 subsystem"
ts8sub = None
rebpssub = None

usets8 = True
try:
    ts8sub  = CCS.attachSubsystem("%s" % ts8);
    rebpssub  = CCS.attachSubsystem("rebps");
except:
    usets8 = False

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

time.sleep(3.)

cdir = tsCWD

raft = UNITID

runnum = "no-eTrav"
try:
    runnum = RUNNUM
except:
    pass


ts_version = ""
ts8_version = ""
power_version = ""

ts_revision = ""
ts8_revision = ""
power_revision = ""


# get the software versions to include in the data products to be persisted in the DB                                                        
ts_version,ts8_version,power_version,ts_revision,ts8_revision,power_revision = eolib.EOgetTS8CCSVersions(tssub,cdir)

# prepare TS8: make sure temperature and vacuum are OK and load the sequencer                                                                
rafttype = "ITL"

if usets8:
    try:
    #    eolib.EOTS8Setup(tssub,ts8sub,rebpssub,raft,rafttype,ccdnames,ccdmanunames,cdir,sequence_file,vac_outlet)
        eolib.EOTS8Setup(tssub,ts8sub,rebpssub,raft,rafttype,cdir,sequence_file,vac_outlet)
    
        print "REBs appear to be attached and ready for exposure. Shutter control will be done via REBs"
    except Exception, ex:
        print "EOTS8Setup failed on %s" % str(ex)
        usets8 = False

if not usets8 :
    print "REBs appear not be be attached or ready for exposure. Perform test using mono shutter only."


print "Setting the current range on the PD device"
pdsub.synchCommand(10,"setCurrentRange",0.000002)

imcount = 1
seq = 0

#number of PLCs between readings
nplc = 1
ccd = CCDID

# flat file pattern
# E2V-CCD250-179_flat_0065.07_flat2_20161130064552.fits
flat_pat = '${sensorLoc}_%07.2fs_${ImageType}%d_${RunNumber}_${timestamp}.fits'
#flat_pat = '${CCDSerialLSST}_${testType}_%07.2fs_${imageType}%d_${RunNumber}_${timestamp}.fits'

if usets8 :
    rply = monosub.synchCommand(900,"openShutter").getResult();
else :
    rply = monosub.synchCommand(900,"closeShutter").getResult();

print "Working on CCD %s" % ccd

print "set filter position"
try:
    monosub.synchCommand(36,"setFilter",1); # open position
except:
    print "Taking longer than it should to move filter wheel to position 1. Not critical."

try:


    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");

    print "Scan at a low and a high wavelength to test monochromator and filter wheel"
    for wl in [450.,450.,450.,823.] :

            target = float(wl)
            print "target wl = %f" % target;

            exptime = 3.0

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

            monosub.synchCommand(60,"setTimeout",300.);

            imdone = 0
            for i in range(imcount):
                print "starting acquisition step for lambda = %8.2f" % wl

                print "Setting the monochromator wavelength and filter"
#                print "You should HEAR some movement"
                result = monosub.synchCommand(240,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");

                print "getting filter wheel setting"
                result = monosub.synchCommand(60,"getFilter");
                ifl = result.getResult()
                print "The wavelength is at %f and the filter wheel is at %f " % (rwl,ifl)
                time.sleep(4.);
                

# adjust timeout because we will be waiting for the data to become ready
                mywait = nplc/60.*nreads*1.5;
                print "Setting timeout to %f s" % mywait
                pdsub.synchCommand(1000,"setTimeout",mywait);

                print "Starting Photo Diode recording at %f" % time.time()
                print "You should see digits changing on the PD device"
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()


# make sure to get some readings before the state of the shutter changes       
                time.sleep(2.0);
 
                timestamp = time.time()
                if usets8 :

                    print "Ready to take image with exptime = %f at time = %f" % (exptime,time.time())

                    acqname = "preflight"
                    ts8sub.synchCommand(10,"setDefaultImageDirectory","%s/S${sensorLoc}" % (cdir));
            
                    ts8sub.synchCommand(10,"setRaftName",str(raft))
                    ts8sub.synchCommand(10,"setRunNumber",runnum)
            
                    ts8sub.synchCommand(10,"setTestType",acqname.lower())
                    ts8sub.synchCommand(10,"setImageType",acqname.lower())
                    ts8sub.synchCommand(10,"setSeqInfo",seq)
                    ts8sub.synchCommand(10,"setFitsFileNamePattern",flat_pat % (exptime,imdone+1))
#                    eolib.EOTS8SetupCCDInfo(ts8sub,rebpssub,ccdnames,ccdmanunames)

                    doLight = True
                    doXED = True
                    fitsfiles = ts8sub.synchCommand(100,"exposeAcquireAndSave",int(exptime*1000),doLight,doXED).getResult();
                    print fitsfiles
                else :

                    rply = monosub.synchCommand(900,"openShutter").getResult();
                    time.sleep(exptime)
                    rply = monosub.synchCommand(900,"closeShutter").getResult();


                print "Done exposing at %f" % time.time()

                print "done with exposure # %d" % i
                print "retrieving photodiode readings at time = %f" % time.time();

                pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (int(timestamp),seq,i+1)
# the primary purpose of this is to guarantee that the accumBuffer method has completed
                print "starting the wait for an accumBuffer done status message at %f" % time.time()
                tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                time.sleep(10.)

                print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                result = pdsub.synchCommand(1000,"readBuffer","/%s/%s" % (cdir,pdfilename),"ts8prod@ts8-raft1");
#                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()
#               time.sleep(10)

# reset timeout to something reasonable for a regular command
                pdsub.synchCommand(1000,"setTimeout",10.);

                imdone += 1

            seq = seq + 1

    fpfiles.close();
    fp.close();

    rply = monosub.synchCommand(900,"openShutter").getResult();
    fp = open("%s/status.out" % (cdir),"w");
# leave in a safe and ready state
    result = monosub.synchCommand(240,"setWaveAndFilter",500.0);
    pdsub.synchCommand(10,"setCurrentRange",0.0000002)

    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % "NA");
    fp.write("%s\n" % "NA");
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.write("%s\n" % power_version);
    fp.write("%s\n" % power_revision);
    fp.close();


# make sure to leave the monochromator shutter open
    rply = monosub.synchCommand(900,"openShutter").getResult();
# get the glowing vacuum gauge back on
#    print "turning the vacuum gauge back on"
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();

    print " =====================================================\n"
    print "            PREFLIGHT DATA ACQUISITION DONE\n"
    print "          CHECK FOR A WIDGET APPEARING THAT WILL\n"
    print "           INDICATE WHETHER THE DATA LOOKS OK\n"
    print " =====================================================\n"

except Exception, ex:

# move TS to ready state                    
#    tssub.synchCommand(60,"setTSIdle");

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
    rply = monosub.synchCommand(900,"openShutter").getResult();
    result = pdsub.synchCommand(30,"softReset");
    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, ex:

# move TS to idle state                    
#    tssub.synchCommand(60,"setTSIdle");

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
    rply = monosub.synchCommand(900,"openShutter").getResult();
    result = pdsub.synchCommand(10,"softReset");
    raise Exception("There was a ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "preflight_acq: COMPLETED"
