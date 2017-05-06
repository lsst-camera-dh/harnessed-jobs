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
    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);
    result = pwrsub.synchCommand(20,"setNamedPowerOn %d heater True" % idx).getResult();

    result = rebsub[id].synchCommand(10,"setHeaterPower %s 0" % (id,'master')).getResult();

    idx = idx + 1

istate = tssub.synchCommand(10,"getstate").getResult()
istate = istate or (jobname.split("__")[1] << 24)
tssub.synchCommand(10,"setstate",istate)

fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
