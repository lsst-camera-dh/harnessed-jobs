###############################################################################
#
#   - Homer
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

cdir = tsCWD


rebsub = {}
serial_number = {}
ts8sub  = CCS.attachSubsystem("ts8");
tssub  = CCS.attachSubsystem("ts");
cryosub  = CCS.attachSubsystem("ts/Cryo");
#pwrsub  = CCS.attachSubsystem("rebps");
#pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0
target_temp_cold = -45.
target_temp_cryo = -160.

cryosub.synchCommand(10,"setSetPoint 1 %f" % target_temp_cold)
cryosub.synchCommand(10,"setSetPoint 2 %f" % target_temp_cryo)
ts8sub.synchCommand(10,"stopTempControl")

while(True) :
    temp = float(cryosub.synchCommand(10,"getTemp B").getResult())

    tdev = abs(temp-target_temp_cold)

    print "target_temp = %f , current cold plate temp = %f , tdev = %f " % (target_temp_cold, temp, tdev) 

    if (tdev < 1.0) :
        break

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
ext = int(jobname.split("__")[1])
if ext>100 :
    ext = ext - 100
istate = (istate & 0xffffff) | (ext << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

fp = open("%s/status.out" % (cdir),"w");

fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
