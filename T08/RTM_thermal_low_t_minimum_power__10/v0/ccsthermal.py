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
cryosub  = CCS.attachSubsystem("ts/Cryo");
pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0
for id in rebdevs:
    try:
        rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);
        
        serial_number[id] = rebsub[id].synchCommand(10,"getSerialNumber").getResult()

        stat = ts8sub.synchCommand(300,"R00.Reb%d setBackBias false" % idx).getResult()
        stat = ts8sub.synchCommand(300,"powerOff %d" % idx).getResult()
        result = pwrsub.synchCommand(20,"setNamedPowerOn %d master False" % idx).getResult();
    except:
        pass

    time.sleep(3.0)

    idx = idx + 1

target_temp = -134.

cryosub.synchCommand(10,"setSetPoint 2 %f" % target_temp)
ts8sub.synchCommand(10,"stopTempControl")

while(True) :
    temp = cryosub.synchCommand(10,"getTemp C")

    tdev = abs(temp-target_temp)

    print "target_temp = %f , current cryo plate temp = %f , tdev = %f " % (target_temp, temp, tdev) 

    if (tdev < 0.2) :
        break

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
istate = (istate & 0xffffff) | (int(jobname.split("__")[1]) << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

fp = open("%s/status.out" % (cdir),"w");

fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
