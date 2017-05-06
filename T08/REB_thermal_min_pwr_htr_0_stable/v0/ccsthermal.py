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
istate = istate or (jobname.split("__")[1] << 24)
tssub.synchCommand(10,"setstate",istate)


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
