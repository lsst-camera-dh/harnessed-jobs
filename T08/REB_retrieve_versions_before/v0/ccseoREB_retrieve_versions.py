###############################################################################
# For use with the harnessed job for retrieving the firmware version
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);


rebsub = []
ts8sub  = CCS.attachSubsystem("ts8");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

fpr = open("%s/REB_versions.txt" % (cdir),"w");
for id in rebdevs:
    try:
        rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);
        firmware_version[id] = rebsub[id].synchCommand(10,"getHwVersion").getResult()
        serial_number[id] = rebsub[id].synchCommand(10,"getSerialNumber").getResult()
        print "Firmware version for REB (S/N=%x) at address %d is %x" % (id,serial_number[id],firmware_version[id])
        fpr.write("%s %x %x\n" % (id,serial_number[id],firmware_version[id]));
    except:
        print "Failed to retrieve firmware version for %s" % id

fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
result = tssub.synchCommandLine(10,"getstate");
istate=result.getResult();
fp.write(`istate`+"\n");
fp.write("%s\n" % ts_version);
fp.write("%s\n" % ts_revision);
fp.write("%s\n" % ts8_version);
fp.write("%s\n" % ts8_revision);
fp.close();


print "REB_retieve_versions: COMPLETED"
