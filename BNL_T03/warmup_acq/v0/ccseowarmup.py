###############################################################################
# warmup_acq
# - turn off cryotiger and control the warm-up
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
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "attaching Lamp subsystem"
    lampsub = CCS.attachSubsystem("%s/Lamp" % ts );
    print "attaching Bias subsystem"
    biassub = CCS.attachSubsystem("%s/Bias" % ts );
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);

    time.sleep(3.)

    cdir = tsCWD

# turn off the lamp
    print "TURNING OFF THE LAMP"
    result = lampsub.synchCommand(100000,"setLampPowerEnable",False);

# turn off power to the cryotiger
    print "TURNING OFF THE POWER TO THE POLYCOLD"
    result = pdusub.synchCommand(120,"setOutletState",cryo_outlet,False);
    rply = result.getResult();

# set bias voltage off
    print "TURNING OFF THE BACKPLANE BIAS VOLTAGE"
    result = biassub.synchCommand(30,"setVoltage",0.0);

# make sure we leave the power to the sensor OFF
    print "POWERING OFF THE CCD"
    result = arcsub.synchCommand(30,"powerOffCCD");

# move to TS idle state ... this will set the cryocon to warm
    print "SETTING STATE OF TESTSTAND TO IDLE"
    result = tssub.synchCommand(100000,"setTSIdle");
    rply = result.getResult();



except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)


print "TS3_warmup: COMPLETED"
