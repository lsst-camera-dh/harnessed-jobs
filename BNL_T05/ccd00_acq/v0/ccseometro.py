###############################################################################
# metro_acq
# METROLOGY SCAN
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

doarch = True


#attach CCS subsystem Devices for scripting
print "Attaching METROLOGY subsystems"
ts5sub  = CCS.attachSubsystem("metrology");


cdir = tsCWD

ts5sub.synchCommand(30,"setCfgStateByName CCD00")

ts5sub.synchCommand(3000,"noStepScan  %s/ccd00.dat" % cdir)


fp = open("%s/status.out" % (cdir),"w");

ts_version = "NA"
ts_revision = "NA"
archon_version = "NA"
archon_revision = "NA"


istate=0;
#result = tssub.synchCommandLine(10,"getstate");
#istate=result.getResult();
fp.write(`istate`+"\n");
fp.write("%s\n" % ts_version);
fp.write("%s\n" % ts_revision);
fp.write("%s\n" % archon_version);
fp.write("%s\n" % archon_revision);
fp.close();


    print " =====================================================\n"
    print "            METROLOGY SCAN DONE\n"
    print " =====================================================\n"

except Exception, ex:

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

except ScriptingTimeoutException, ex:

    raise Exception("There was a ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)


print "metro_acq: COMPLETED"
