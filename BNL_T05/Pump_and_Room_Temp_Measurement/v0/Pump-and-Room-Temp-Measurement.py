###############################################################################
# Pump_and_Room_Temp_Measurement
# TS5 KEYENCE METROLOGY SCAN
#      Date: 11/07
#      Authors: Homer and Rebecca
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);


#attach CCS subsystem Devices for scripting
print "Attaching METROLOGY subsystems"
ts5sub  = CCS.attachSubsystem("metrology");
print "Attaching CRYO subystems"
cryosub = CCS.attachSubsystem("%s/Cryo" % ts );


cdir = tsCWD

target_temp = 20. 

cur_temp = cryosub.synchCommand(20,"getTemp B").getResult())

# number of degrees per minute
trate = 1.0

# duration in seconds
period = (target_temp - cur_temp) / (trate/60.0); 

# steps
# - lets do one for every degree
nsteps = abs(target_temp - cur_temp)


########################################################################################
# Check Pressure
    starttim = time.time()
    while True:
        print "checking if pressure is low enough to turn on turbo pump";
        result = vacsub.synchCommand(20,"readPressure");
        pres = result.getResult();
        print "time = %f , P = %f\n" % (time.time(),pres)
        if ((time.time()-starttim)>7200):
            print "Something is wrong ... we will never make it to a low enough pressure for turning on the turbo pump"
            exit
        if (pres>0.0 and pres<1.0) :
            break
        time.sleep(5.)

# Turn on power to the turbo pump
    result = vacsub.synchCommand(20,"readPressure");
    pres = result.getResult();
    if (pres>0.0 and pres<1.0) :
        print "TURNING ON POWER TO THE TURBO PUMP!"
        result = pdusub.synchCommand(120,"setOutletState",pump_outlet,True);
        rply = result.getResult();
########################################################################################



cryosub.synchCommand(20,"rampTemp",period,target_temp,nsteps).getResult()

ts5sub.synchCommand(30,"setCfgStateByName RTM")

tstart = time.time()
start_temp = {}
for temp in ["A","B","C","D"]:
    start_temp.append(cryosub.synchCommand(20,"getTemp %s" % temp).getResult())

ts5sub.synchCommand(3000,"noStepScan  %s/RSA-warm-1.dat" % cdir)

tstop = time.time()
stop_temp = {}
for temp in ["A","B","C","D"]:
    stop_temp.append(cryosub.synchCommand(20,"getTemp %s" % temp).getResult())

fpdat = open("%s/RSA-warm-1.dat" % (cdir),"a");
fpdat.write("start time = %f , stop time = %f\n" % (tstart,tstop))
for temp in ["A","B","C","D"]:
    fpdat.write("temperature %s at start %f C at end %f C\n" % (temp,start_temp[idx],stop_temp[idx]))

fpdat.close()

fp = open("%s/status.out" % (cdir),"w");

ts_version = "NA"
ts_revision = "NA"
ts5_version = "NA"
ts5_revision = "NA"


istate=0;
fp.write(`istate`+"\n");
fp.write("%s\n" % ts_version);
fp.write("%s\n" % ts_revision);
fp.write("%s\n" % ts5_version);
fp.write("%s\n" % ts5_revision);
fp.close();


print " =====================================================\n"
print "            TS5 KEYENCE METROLOGY SCAN DONE\n"
print " =====================================================\n"


print "Pump_and_Room_Temp_Measurement: COMPLETED"
