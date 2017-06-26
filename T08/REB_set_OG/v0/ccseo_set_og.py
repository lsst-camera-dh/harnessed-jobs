###############################################################################
# For use with the harnessed job for setting og 
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

fpsettings = open("%s/og_settings.txt" % (cdir),"r");
for line in fpsettings:
    if "OG" in line :
        setOG = line.split()[1]
fpsettings.close()



fpr = open("%s/REB_og.txt" % (cdir),"w");
for id in rebdevs:
#    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);

    for ii in range(3) :

        
        subsys = "ts8/%s.Bias%d" % (id,ii)
        print "Attaching %s" % subsys
        rebbiassub  = CCS.attachSubsystem(subsys);
        print "new OG = ",setOG
        print rebbiassub.synchCommand(10,"change ogP %s" % setOG).getResult()

        print "New parameters for %s_%d : " % (id,ii),rebbiassub.synchCommand(10,"printConfigurableParameters []").getResult()

time.sleep(1.0)

print ts8sub.synchCommand(10,"loadDacs true").getResult()
print ts8sub.synchCommand(10,"loadBiasDacs true").getResult()

time.sleep(2.0)

for id in rebdevs:
    for ii in range(3) :
        OG = ts8sub.synchCommand(10,"getChannelValue %s.OG%dV" % (id,ii)).getResult()
        fpr.write("%s %f\n" % (str(id)+"_"+str(ii),OG));


fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "REB_retieve_versions: COMPLETED"
