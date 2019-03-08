###############################################################################
# RTM warmup script stage 1
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

pwrsub  = CCS.attachSubsystem("rebps");
pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");


print "powering off sensors"
print "openning HV bias switch"
rply = ts8sub.synchCommand(10,"setBackBias false").getResult()
print ts8sub.synchCommand(10,"isBackBiasOn").getResult()

for id in rebdevs:

    idx = int(id[len(id)-1])

    print "REB number = ",idx

    try:
        rebsub[id]  = CCS.attachSubsystem("%s/%s" % (ts8,id));
        
        print "verifying REB connection"
        serial_number[id] = rebsub[id].synchCommand(10,"getSerialNumber").getResult()
        print "serial number = ",serial_number[id]
        print "powering off sensors"
        print ts8sub.synchCommand(300,"powerOff %d" % idx).getResult()

    except:
        pass


print "setting RSA heater power"

stat = ts8sub.synchCommand(300,"stopTempControl").getResult()

idx = 0
for id in rebdevs:
    rebsub[id]  = CCS.attachSubsystem("%s/%s" % (ts8,id));
    result = rebsub[id].synchCommand(10,"setHeaterPower 0 0.8").getResult();

# make sure the heaters are powered
result = pwrsub.synchCommand(20,"setNamedPowerOn 0 heater True").getResult();
result = pwrsub.synchCommand(20,"setNamedPowerOn 2 heater True").getResult();

# make sure the plate heaters are set to the correct range
result = cryosub.synchCommand(20,"setHeaterRange 1 \"Hi\"").getResult()
result = cryosub.synchCommand(20,"setHeaterRange 2 \"Hi\"").getResult()


last_cold_temp = -999.
last_cryo_temp = -999.
last_ccd_temp = -999.

tstep = 1.0
safetymargin = 7

print "temperature step (C) = ",tstep
print "safety margin (i.e. min CCD temperature w.r.t. cryo plate) (C) = ",safetymargin

# start raising the temperature in steps while monitoring for any reason to pause
while (True) :
    try:
        cold_tempa = cryosub.synchCommand(20,"getTemp A").getResult()
        cold_tempb = cryosub.synchCommand(20,"getTemp B").getResult()
        cryo_temp = cryosub.synchCommand(20,"getTemp C").getResult()
        ccd_temp1 = ts8sub.synchCommand(20,"getChannelValue R00.Reb0.CCDTemp1").getResult()
        ccd_temp2 = ts8sub.synchCommand(20,"getChannelValue R00.Reb2.CCDTemp1").getResult()
        cryosetpt = cryosub.synchCommand(20,"getSetPoint 2").getResult()

        pressure = vacsub.synchCommand(20,"readPressure").getResult();
    except:
        print "failed to retrieve environment data"
        time.sleep(5.0)
        continue

    ccd_temp = min(ccd_temp1,ccd_temp2)


    if (cryo_temp < -273. or cold_tempa < -273. or cold_tempb < 273.):
        print "c1"
        if (ccd_temp < -273. or cryosetpt < -273. or pressure < 1.0e-10) :
            print "time = %d, ccd_temp = %f, cryo_temp  %f, cryosetpt = %f, pressure = %11.3e" % (time.time(),ccd_temp,cryo_temp,cryosetpt,pressure)
            print "bad thermal status data received"
            print "retrying in 10 seconds"
            time.sleep(30.0)
            continue



    if ((ccd_temp-cryo_temp-tstep) > safetymargin and pressure < .00005 and (ccd_temp+tstep)<20.0) :
        print "updating setpoint"
        cryosub.synchCommand(20,"setSetPoint",2,cryo_temp+tstep).getResult()
    else:
        print "(ccd_temp-cryo_temp-tstep) > safetymargin : ",(ccd_temp-cryo_temp-tstep) > safetymargin
        print "pressure < .00005 : ",pressure < .00005
        print " (ccd_temp+tstep)<20.0) : ",(ccd_temp+tstep)<20.0

    cryosetpt = cryosub.synchCommand(20,"getSetPoint 2").getResult()

    print "time = %d, ccd_temp = %f, cryo_temp  %f, cryosetpt = %f, pressure = %11.3e" % (time.time(),ccd_temp,cryo_temp,cryosetpt,pressure)

    if (ccd_temp > cold_tempa and ccd_temp > cold_tempb) :
         print "warming step 1 is now complete .... proceed to turn off the PT-30"
         break
    if ((cryosetpt+tstep)>15.) :
        for id in rebdevs:

            idx = int(id[len(id)-1])

            rebsub[id]  = CCS.attachSubsystem("%s/%s" % (ts8,id));
            result = pwrsub.synchCommand(20,"setNamedPowerOn %d heater True" % idx).getResult();
            result = rebsub[id].synchCommand(10,"setHeaterPower 0 0.0").getResult();
            idx = idx + 1
        print "warming step 2 is now complete .... proceed to turn off the PT-30"
        break

    time.sleep(60.0)
    last_cold_temp = cold_tempb
    last_cryo_temp = cryo_temp
    last_ccd_temp = ccd_temp


istate = 1
#print "istate after = ",istate
#tssub.synchCommand(10,"setstate",istate)


#fp = open("%s/status.out" % (cdir),"w");
#fp.write(`istate`+"\n");
#fp.close();


print "COMPLETED"
