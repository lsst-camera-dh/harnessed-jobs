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
ts8sub  = CCS.attachSubsystem("%s" % ts8);
tssub  = CCS.attachSubsystem("ts");
cryosub  = CCS.attachSubsystem("ts/Cryo");
pwrsub  = CCS.attachSubsystem("rebps");
pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0
for id in rebdevs:
    try:
        rebsub[id]  = CCS.attachSubsystem("%s/%s" % (ts8,id));
        
        serial_number[id] = rebsub[id].synchCommand(10,"getSerialNumber").getResult()

        stat = ts8sub.synchCommand(300,"R00.Reb%d setBackBias false" % idx).getResult()
        stat = rebsub[id].synchCommand(300,"powerCCDsOff").getResult()
        result = pwrsub.synchCommand(20,"sequencePower %d False" % idx).getResult();
    except:
        pass

    time.sleep(3.0)

    idx = idx + 1

target_temp = -126.
#target_temp = -114.

cryosub.synchCommand(10,"setSetPoint 2 %f" % target_temp)
ts8sub.synchCommand(10,"stopTempControl")

while(True) :
    temp = float(cryosub.synchCommand(10,"getTemp C").getResult())

    tdev = abs(temp-target_temp)

    print "target_temp = %f , current cryo plate temp = %f , tdev = %f " % (target_temp, temp, tdev) 

    if (tdev < 2.0) :
        break


istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
ext = int(jobname.split("__")[1])
if ext>400 :
    ext= ext - 400
istate = (istate & 0xffffff) | (ext << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)


fp = open("%s/status.out" % (cdir),"w");

fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
