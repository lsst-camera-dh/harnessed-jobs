###############################################################################
# Room-Temp-Measurement-After-Thermal-Cycle
# TS5 KEYENCE METROLOGY SCAN
#      Date: 11/07
#      Authors: Homer and Rebecca
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import os
import sys
import time
#import eolib

CCS.setThrowExceptions(True);


#attach CCS subsystem Devices for scripting
print "Attaching METROLOGY subsystems"
ts5sub  = CCS.attachSubsystem("metrology");
print "Attaching CRYO subystems"
cryosub = CCS.attachSubsystem("ts/Cryo" );
vacsub = CCS.attachSubsystem("ts/VQMonitor");
pdusub = CCS.attachSubsystem("ts/PDU");

runnum = "no-eTrav"
try:
    RUNNUM = os.environ['LCATR_RUN_NUMBER']
    runnum = RUNNUM
except:
    pass


#cdir = tsCWD
cdir = os.getcwd()
UNITID = os.environ['LCATR_UNIT_ID']


target_temp = 20. 

cur_temp = cryosub.synchCommand(20,"getTemp B").getResult()
#cur_temp = 20.

# number of degrees per minute
trate = 1.2

# duration in seconds
period = abs(target_temp - cur_temp) / (trate/60.0); 

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

#    pdusub.synchCommand(120,"setOutletState",cryo_outlet,False).getResult()

        cryosub.synchCommand(40000,"rampTemp %f %f %d" % (period,target_temp,nsteps)).getResult()

        while (True) :
            now_temp = cryosub.synchCommand(20,"getTemp B").getResult()
            if (abs(target_temp-now_temp)<2.0) :
                break
            time.sleep(5.0)
            print "waiting for target temp to be reached. current temp = %fC" % now_temp

ts5sub.synchCommand(30,"setCfgStateByName BASEPLATE")

tstart = time.time()

aa=time.ctime().split(" ")
tstart_human = (aa[4]+aa[1]+aa[2]+"-"+aa[3]).replace(":","")
fln = "%s_WarmColdMet_%s_%s_%dC.csv" % (UNITID,runnum,tstart_human,target_temp)

start_temp = {}

for temp in ["A","B","C","D"]:
    start_temp[temp]=cryosub.synchCommand(20,"getTemp %s" % temp).getResult()
#    start_temp[temp]=20.0

#ts5sub.synchCommand(3000,"scanfl %s/Room-Temp-Measurement-After-Thermal-Cycle.dat" % cdir)
ts5sub.synchCommand(6000,"scanfl %s/%s" % (cdir,fln))

tstop = time.time()
stop_temp = {}
for temp in ["A","B","C","D"]:
    stop_temp[temp]=cryosub.synchCommand(20,"getTemp %s" % temp).getResult()
#    stop_temp[temp]=20.0

#fpdat = open("%s/Room-Temp-Measurement-After-Thermal-Cycle.dat" % (cdir),"a");
fpdat = open("%s/%s" % (cdir,fln),"a");
fpdat.write("# start time = %f , stop time = %f\n" % (tstart,tstop))
for temp in ["A","B","C","D"]:
    fpdat.write("# temperature %s at start %f C at end %f C\n" % (temp,start_temp[temp],stop_temp[temp]))

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


print "Room-Temp-Measurement-After-Thermal-Cycle: COMPLETED"
