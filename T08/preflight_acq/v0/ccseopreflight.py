###############################################################################
# preflight_acq
# test the test stand for readiness
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);


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

time.sleep(3.)

cdir = tsCWD

ts_version = ""
ts8_version = ""
ts_revision = ""
ts8_revision = ""

ts_version,ts8_version,ts_revision,ts8_revision = eolib.EOgetCCSVersions(tssub,cdir)

# make sure the BSS is off
biassub.synchCommand(10,"setVoltage",0.0)

#eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub,"setTSIdle","setTSIdle")

print "Setting the current ranges on the Bias and PD devices"
biassub.synchCommand(10,"setCurrentRange",0.0002)
pdsub.synchCommand(10,"setCurrentRange",0.00002)

imcount = 1

seq = 0

#number of PLCs between readings
nplc = 1

ccd = CCDID
result = arcsub.synchCommand(10,"setCCDnum",ccd)
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

            for i in range(imcount):
                print "starting acquisition step for lambda = %8.2f" % wl

                print "Setting the monochromator wavelength and filter"
#                print "You should HEAR some movement"
                result = monosub.synchCommand(240,"setWaveAndFilter",wl);
                rwl = result.getResult()
                time.sleep(10.)
                print "publishing state"
                result = tssub.synchCommand(60,"publishState");

                result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)

                print "getting filter wheel setting"
                result = monosub.synchCommand(60,"getFilter");
                ifl = result.getResult()
                print "The wavelength is at %f and the filter wheel is at %f " % (rwl,ifl)
                time.sleep(4.);
                

# adjust timeout because we will be waiting for the data to become ready
                mywait = nplc/60.*nreads*1.10 ;
                print "Setting timeout to %f s" % mywait
                pdsub.synchCommand(1000,"setTimeout",mywait);

                print "Starting Photo Diode recording at %f" % time.time()
                print "You should see digits changing on the PD device"
                pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);

                print "recording should now be in progress and the time is %f" % time.time()


# make sure to get some readings before the state of the shutter changes       
                time.sleep(2.0);
 
                result = monosub.synchCommand(900,"openShutter");
                rwl = result.getResult()
                time.sleep(exptime)
                result = monosub.synchCommand(900,"closeShutter");
                rwl = result.getResult()

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
                result = pdsub.synchCommand(1000,"readBuffer","%s/%s" % (cdir,pdfilename));
                buff = result.getResult()
                print "Finished getting readings at %f" % time.time()

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
    tssub.synchCommand(60,"setTSIdle");

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
    result = pdsub.synchCommand(10,"softReset");
    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, ex:

# move TS to idle state                    
#    tssub.synchCommand(60,"setTSIdle");

# get the glowing vacuum gauge back on
#    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
#    rply = result.getResult();
    result = pdsub.synchCommand(10,"softReset");
    raise Exception("There was a ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "preflight_acq: COMPLETED"
