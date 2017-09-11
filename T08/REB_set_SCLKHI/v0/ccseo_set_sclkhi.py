###############################################################################
# For use with the harnessed job for setting sclkHI 
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

cdir = tsCWD


#rebsub = {}
firmware_version = {}
serial_number = {}
ts8sub  = CCS.attachSubsystem("ts8");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

fpsettings = open("%s/sclkhi_settings.txt" % (cdir),"r");
for line in fpsettings:
    if "SCLKHI" in line :
        setSCLKHI = line.split()[1]
fpsettings.close()



fpr = open("%s/REB_sclkhi.txt" % (cdir),"w");
for id in rebdevs:
#    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);

    subsys = "ts8/%s.DAC" % (id)
    print "Attaching %s" % subsys
    rebdacsub  = CCS.attachSubsystem(subsys);
    print "new SCLKHI = ",setSCLKHI
    print rebdacsub.synchCommand(10,"change sclkHighP %s" % setSCLKHI).getResult()

    print "New parameters for %s : " % (id),rebdacsub.synchCommand(10,"printConfigurableParameters []").getResult()

time.sleep(1.0)

print ts8sub.synchCommand(10,"loadDacs true").getResult()
print ts8sub.synchCommand(10,"loadBiasDacs true").getResult()

time.sleep(2.0)

for id in rebdevs:
    SCLKHI = ts8sub.synchCommand(10,"getChannelValue %s.SClkU" % id).getResult()
    fpr.write("%s %f\n" % (str(id),SCLKHI));


fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "REB_retieve_versions: COMPLETED"
