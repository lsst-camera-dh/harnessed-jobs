###############################################################################
# ts3_pump
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
        print "checking if pressure is low enough to turn on turbo pump";
        result = vacsub.synchCommand(20,"readPressure");
        pres = result.getResult();
        print "time = %f , P = %f\n" % (time.time(),pres)
        if ((time.time()-starttim)>3600):
            print "Something is wrong ... we will never make it to a runnable state"
            exit
        if (pres>0.0 and pres<5.5e-2) :
            break
        time.sleep(5.)

# turn on power to the turbo pump
    result = vacsub.synchCommand(20,"readPressure");
    pres = result.getResult();
    if (pres>0.0 and pres<5.5e-2) :
        print "TURNING ON POWER TO THE TURBO PUMP!"
        result = pdusub.synchCommand(120,"setOutletState",pump_outlet,True);
        rply = result.getResult();


except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, ex:

    raise Exception("There was an ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % archon_version);
    fp.write("%s\n" % archon_revision);
    fp.close();

print "ts3_pump: COMPLETED"
