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
pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

idx = 0
for id in rebdevs:
    rebsub[id]  = CCS.attachSubsystem("ts8/%s" % id);
    result = pwrsub.synchCommand(20,"setNamedPowerOn %d heater True" % idx).getResult();

    result = rebsub[id].synchCommand(10,"setHeaterPower 0 1.0").getResult();

    idx = idx + 1

last_cold_temp = -999.
last_cryo_temp = -999.
last_ccd_temp = -999.


for iiter in range(20) :
    cold_temp = cryosub.synchCommand(20,"getTemp B").getResult()
    cryo_temp = cryosub.synchCommand(20,"getTemp C").getResult()
    ccd_temp = ts8sub.synchCommand(20,"getChannelValue R00.Reb1.CCDTemp1").getResult()

    print "iiter = %d, delta_cold = %f, delta_cryo = %f, delta_ccd = %f" % (iiter,cold_temp-last_cold_temp,cryo_temp-last_cryo_temp,ccd_temp-last_ccd_temp)

    if (abs(last_cold_temp-cold_temp)<0.1 and abs(last_cryo_temp-cryo_temp) < 0.1 and abs(last_ccd_temp-ccd_temp)<0.1) :
        break

    time.sleep(180.0)
    last_cold_temp = cold_temp
    last_cryo_temp = cryo_temp
    last_ccd_temp = ccd_temp


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
