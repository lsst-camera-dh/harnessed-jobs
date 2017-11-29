###############################################################################
# For use with the harnessed job for retrieving the firmware version
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

cdir = tsCWD


rebsub = {}
firmware_version = {}
serial_number = {}
ts8sub  = CCS.attachSubsystem("%s" % ts8);
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

fpr = open("%s/REB_versions.txt" % (cdir),"w");
for id in rebdevs:
    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);
    firmware_version[id] = rebsub[id].synchCommand(10,"getHwVersion").getResult()
    serial_number[id] = rebsub[id].synchCommand(10,"getSerialNumber").getResult()
    print "Firmware version for REB (S/N=%x) at address %s is %x" % (serial_number[id],id,firmware_version[id])
    try:
        fpr.write("%s %x %x\n" % (id,serial_number[id],firmware_version[id]));
    except:
        print "Failed to retrieve firmware version for %s" % id

fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "REB_retieve_versions: COMPLETED"
