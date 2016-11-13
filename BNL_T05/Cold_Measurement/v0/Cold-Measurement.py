###############################################################################
# Cold-Measurement
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
#print "Attaching CRYO subystems"
#cryosub = CCS.attachSubsystem("ts/Cryo" );


cdir = tsCWD

target_temp = -30. 

#cur_temp = cryosub.synchCommand(20,"getTemp B").getResult()
cur_temp = 20.

# number of degrees per minute
trate = 1.0

# duration in seconds
period = (target_temp - cur_temp) / (trate/60.0); 

# steps
# - lets do one for every degree
nsteps = abs(target_temp - cur_temp)

###################################################################
# Once at a safe pressure, begin cooling the device
starttim = time.time()
if (False):
    while True:
        result = vacsub.synchCommand(20,"readPressure");
        pres = result.getResult();
        print "time = %f , P = %f\n" % (time.time(),pres)
        if (pres>0.0 and pres<0.001) :
            break
        time.sleep(5.)
###################################################################

        cryosub.synchCommand(20,"rampTemp",period,target_temp,nsteps).getResult()


ts5sub.synchCommand(30,"setCfgStateByName RTM")

tstart = time.time()
start_temp = {}

for temp in ["A","B","C","D"]:
#    start_temp.append(cryosub.synchCommand(20,"getTemp %s" % temp).getResult())
    start_temp[temp]=20.0

ts5sub.synchCommand(3000,"noStepScan  %s/Cold-Measurement.dat" % cdir)

tstop = time.time()
stop_temp = {}
for temp in ["A","B","C","D"]:
#    stop_temp[temp]=cryosub.synchCommand(20,"getTemp %s" % temp).getResult()
    stop_temp[temp]=20.0

fpdat = open("%s/Cold-Measurement.dat" % (cdir),"a");
fpdat.write("start time = %f , stop time = %f\n" % (tstart,tstop))
for temp in ["A","B","C","D"]:
    fpdat.write("temperature %s at start %f C at end %f C\n" % (temp,start_temp[temp],stop_temp[idx]))

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


print "Cold-Measurement: COMPLETED"