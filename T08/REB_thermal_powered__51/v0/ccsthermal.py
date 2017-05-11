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

tssub  = CCS.attachSubsystem("ts");

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
istate = (istate & 0xffffff) | (int(jobname.split("__")[1]) << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

time.sleep(3600.0)

fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
