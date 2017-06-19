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


#rebsub = {}
firmware_version = {}
serial_number = {}
ts8sub  = CCS.attachSubsystem("ts8");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

fpsettings = open("%s/od_rd_settings.txt" % (cdir),"r");
for line in fpsettings:
    if "OD" in line :
        setOD = line.split()[1]
    if "RD" in line :
        setRD = line.split()[1]
fpsettings.close()



fpr = open("%s/REB_od_rd.txt" % (cdir),"w");
for id in rebdevs:
#    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);

    for ii in range(3) :

        
        subsys = "ts8/%s.Bias%d" % (id,ii)
        print "Attaching %s" % subsys
        rebbiassub  = CCS.attachSubsystem(subsys);
        print "new RD = ",setRD
        print rebbiassub.synchCommand(10,"change rdP %s" % setRD).getResult()
        print "new OD = ",setOD
        print rebbiassub.synchCommand(10,"change odP %s" % setOD).getResult()

        print "New parameters for %s_%d : " % (id,ii),rebbiassub.synchCommand(10,"printConfigurableParameters []").getResult()

time.sleep(1.0)

print ts8sub.synchCommand(10,"loadDacs true").getResult()
print ts8sub.synchCommand(10,"loadBiasDacs true").getResult()

time.sleep(2.0)

for id in rebdevs:
    for ii in range(3) :
        RD = ts8sub.synchCommand(10,"getChannelValue %s.RD%dV" % (id,ii)).getResult()
        OD = ts8sub.synchCommand(10,"getChannelValue %s.OD%dV" % (id,ii)).getResult()

        fpr.write("%s %f %f\n" % (str(id)+"_"+str(ii),RD,OD));


fpr.close()


fp = open("%s/status.out" % (cdir),"w");
istate=0;
fp.write(`istate`+"\n");
fp.close();


print "REB_retieve_versions: COMPLETED"
