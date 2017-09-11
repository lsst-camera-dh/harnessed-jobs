###############################################################################
# For use with the harnessed job for setting gd 
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

fpsettings = open("%s/gd_settings.txt" % (cdir),"r");
for line in fpsettings:
    if "GD" in line :
        setGD = line.split()[1]
fpsettings.close()



fpr = open("%s/REB_gd.txt" % (cdir),"w");
for id in rebdevs:
#    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);

    for ii in range(3) :

        
        subsys = "ts8/%s.Bias%d" % (id,ii)
        print "Attaching %s" % subsys
        rebbiassub  = CCS.attachSubsystem(subsys);
        print "new GD = ",setGD
        print rebbiassub.synchCommand(10,"change gdP %s" % setGD).getResult()

        print "New parameters for %s_%d : " % (id,ii),rebbiassub.synchCommand(10,"printConfigurableParameters []").getResult()

time.sleep(1.0)

print ts8sub.synchCommand(10,"loadDacs true").getResult()
print ts8sub.synchCommand(10,"loadBiasDacs true").getResult()

time.sleep(2.0)

for id in rebdevs:
    for ii in range(3) :
        GD = ts8sub.synchCommand(10,"getChannelValue %s.GD%dV" % (id,ii)).getResult()
        fpr.write("%s %f\n" % (str(id)+"_"+str(ii),GD));


fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "REB_retieve_versions: COMPLETED"
