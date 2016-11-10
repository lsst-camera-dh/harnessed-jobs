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
    print "attaching Cryo subsystem"
    cryosub = CCS.attachSubsystem("%s/Cryo" % ts );
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
    try:
        print "POWERING OFF THE CCD"
        result = arcsub.synchCommand(30,"powerOffCCD");
    except:
        print "Unable to power off the CCD. Perhaps the controller is already off."

# move to TS idle state ... this will set the cryocon to warm
    print "SETTING STATE OF TESTSTAND TO WARM"
    result = tssub.synchCommand(100000,"setTSWarm");
    rply = result.getResult();

# turn off the turbo pump
    starttim = time.time()
    while True:
        print "checking if the temperature is high enough to turn off turbo pump";
        result = cryosub.synchCommand(20,"getTemp","B");
        temp = result.getResult();
        print "time = %f , T = %11.3e\n" % (time.time(),temp)
        if ((time.time()-starttim)>15000):
            print "Something is wrong ... we will never make it to a suitable state"
            exit
        if (temp>5.0 and temp<999.) :
            print "Would be TURNING OFF POWER TO THE TURBO PUMP!"
#            result = pdusub.synchCommand(120,"setOutletState",pump_outlet,False);
#            rply = result.getResult();
            break
        time.sleep(5.)



except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)


print "TS3_warmup: COMPLETED"
