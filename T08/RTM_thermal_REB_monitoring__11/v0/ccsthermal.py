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
pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0
for id in rebdevs:
    result = pwrsub.synchCommand(10,"sequencePower %d True" % (idx)).getResult();
    time.sleep(3.0)

    idx = idx + 1

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
istate = (istate & 0xffffff) | (int(jobname.split("__")[1]) << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
