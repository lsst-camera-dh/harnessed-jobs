###############################################################################
# ts3_cool_down
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
    print "attaching Cryo subsystem"
    cryosub = CCS.attachSubsystem("%s/Cryo" % ts );
    print "attaching VacuumGauge subsystem"
    vacsub = CCS.attachSubsystem("%s/VacuumGauge" % ts );
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);

    time.sleep(3.)

    cdir = tsCWD

# Initialization

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)

    starttim = time.time()
    while True:
        print "checking if pressure is low enough to turn on PolyCold";
        result = vacsub.synchCommand(20,"readPressure");
        pres = result.getResult();
        print "time = %f , pressure = %11.3e\n" % (time.time(),pres)
        if ((time.time()-starttim)>7200):
            print "Something is wrong ... we will never make it to a runnable state"
            exit
        if (pres>0.0 and pres<1.0e-3) :
            break
        time.sleep(5.)

# turn on power to the PolyCold
    result = vacsub.synchCommand(20,"readPressure");
    pres = result.getResult();
    if (pres>0.0 and pres<1.0e-3) :
        print "TURNING ON POWER TO THE POLYCOLD!"
        result = pdusub.synchCommand(120,"setOutletState",cryo_outlet,True);
        rply = result.getResult();

# move TS to ready state
    rdyresult = tssub.asynchCommand("setTSReady");
# let it run in the background

#check state of ts devices
    print "wait for ts state to become ready";
    tsstate = 0
    starttim = time.time()
    fpfiles = open("%s/cooldown.dat" % cdir,"w");

    while True:
        print "checking for test stand to be ready for acq";
        try:
            result = tssub.synchCommand(10,"isTestStandReady");
            tsstate = result.getResult();
            result = cryosub.synchCommand(20,"getTemp","B");
            ctemp = result.getResult();
            tstat = "time = %f , T = %f\n" % (time.time(),ctemp)
            print tstat
            fpfiles.write(tstat)
        except:
            print "likely an attempt to query when an action was in progress"
            print "It is OK ... we caught it."
# the following line is just for test situations so that there would be no waiting
#        tsstate=1;
        if ((time.time()-starttim)>18000):
            print "Something is wrong ... we will never make it to a runnable state"
            exit
        if tsstate!=0 :
            break
        time.sleep(5.)

    fpfiles.close()

# safety check that it really is done
    reply = rdyresult.get();

    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

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

except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, ex:

    raise Exception("There was an ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "ts3_cool_down: COMPLETED"
