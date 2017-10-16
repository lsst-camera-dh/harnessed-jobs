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
#pwrsub  = CCS.attachSubsystem("ccs-rebps");
#pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0

tstep = 10.0
for itim in range(30):
    time.sleep(tstep)
    print "waited %f seconds" % (itim*tstep)

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
