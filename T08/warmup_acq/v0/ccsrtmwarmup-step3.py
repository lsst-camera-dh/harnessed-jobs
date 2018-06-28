###############################################################################
# RTM warmup script stage 2
#   - Homer
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

#cdir = tsCWD
try:
    ts8 = "ts8-otm0"
    ts8sub  = CCS.attachSubsystem("%s" % ts8);
    rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()
except:
    ts8 = "ts8-otm2"
    ts8sub  = CCS.attachSubsystem("%s" % ts8);
    rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

rebsub = {}
serial_number = {}
tssub  = CCS.attachSubsystem("ts");
cryosub  = CCS.attachSubsystem("ts/Cryo");
vacsub = CCS.attachSubsystem("ts/VQMonitor");

pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");


print "powering off REBs:"



print "powering off REB0"
print pwrsub.synchCommand(20,"sequencePower 0 False").getResult();

print "powering off REB1"
print pwrsub.synchCommand(20,"sequencePower 1 False").getResult();

print "powering off REB2"
print pwrsub.synchCommand(20,"sequencePower 2 False").getResult();



last_cold_temp = -999.
last_cryo_temp = -999.


tstep = 1.0
safetymargin = 7

#for iiter in range(12) :
while (True) :
    try:
        cold_tempa = cryosub.synchCommand(20,"getTemp A").getResult()
        cold_tempb = cryosub.synchCommand(20,"getTemp B").getResult()
        cryo_temp = cryosub.synchCommand(20,"getTemp C").getResult()
        coldsetpt = cryosub.synchCommand(20,"getSetPoint 1").getResult()

        pressure = vacsub.synchCommand(20,"readPressure").getResult();
    except:
        print "failed to retrieve environment data"
        time.sleep(5.0)
        continue


    if ((cryo_temp < -273.) or (cold_tempa < -273.) or (cold_tempb < -273.)  or (pressure < 1.0e-10)) :
        print "time = %d, cold_tempa = %f, cold_tempb = %f, coldsetpt = %f, pressure = %11.3e" % (time.time(),cold_tempa,cold_tempb,coldsetpt,pressure)
        print "bad thermal status data received"
        print "retrying in 30 seconds"
        time.sleep(30.0)
        continue



    if (pressure < .0002 and (cold_tempb+tstep)<20.0) :
        print "updating setpoint"
        cryosub.synchCommand(20,"setSetPoint",1,cold_tempb+tstep).getResult()
    else:
        print "pressure < .0002 : ",pressure < .0002
        print " (cold_tempb+tstep)<20.0) : ",(cold_tempb+tstep)<20.0

    coldsetpt = cryosub.synchCommand(20,"getSetPoint 1").getResult()

    print "time = %d, cold_tempa = %f, cold_tempb = %f, coldsetpt = %f, pressure = %11.3e" % (time.time(),cold_tempa,cold_tempb,coldsetpt,pressure)

    if ((cold_tempb+tstep)>20.) :
        print "The final warming step is now complete. The RTM is warm but one should still wait the necessary time for equilibrium before opening the cryostat."
        break

    time.sleep(60.0)
    last_cold_temp = cold_tempb
    last_cryo_temp = cryo_temp



istate = 1
#print "istate after = ",istate
#tssub.synchCommand(10,"setstate",istate)


#fp = open("%s/status.out" % (cdir),"w");
#fp.write(`istate`+"\n");
#fp.close();


print "COMPLETED"
