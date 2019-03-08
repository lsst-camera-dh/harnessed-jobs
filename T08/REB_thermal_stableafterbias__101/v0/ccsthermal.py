###############################################################################
#
#   - Homer
###############################################################################

from org.lsst.ccs.scripting import CCS
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
    rebsub[id]  = CCS.attachSubsystem("%s/%s" % (ts8,id));
    result = pwrsub.synchCommand(20,"setNamedPowerOn %d heater True" % idx).getResult();

    result = rebsub[id].synchCommand(10,"setHeaterPower 0 0.0").getResult();

    idx = idx + 1


time.sleep(3600.0)

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
istate = (istate & 0xffffff) | (int(jobname.split("__")[1]) << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)


fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
