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

def getrsatemp(ts8sub) :
    temp = -999.
    try:
        ccd0temp = ts8sub.synchCommand(10,"getChannelValue R00.Reb0.CCDTemp1").getResult()
        ccd1temp = ts8sub.synchCommand(10,"getChannelValue R00.Reb1.CCDTemp1").getResult()
        ccd2temp = ts8sub.synchCommand(10,"getChannelValue R00.Reb2.CCDTemp1").getResult()
        temp = (ccd0temp + ccd1temp + ccd2temp)/3.0
    except:
        pass
    return temp


CCS.setThrowExceptions(True);


#attach CCS subsystem Devices for scripting
print "Attaching METROLOGY subsystems"
ts5sub  = CCS.attachSubsystem("metrology");
print "Attaching CRYO subystems"
cryosub = CCS.attachSubsystem("ts/Cryo" );
vacsub = CCS.attachSubsystem("ts/VQMonitor");
pdusub = CCS.attachSubsystem("ts/PDU");
ts8sub   = CCS.attachSubsystem("ts8");

runnum = "no-eTrav"
try:
    runnum = RUNNUM
except:
    pass


cdir = tsCWD

target_temp = -100. 

cur_temp = getrsatemp(ts8sub)
if (cur_temp < -273.) :
    cur_temp = cryosub.synchCommand(20,"getTemp B").getResult()


#cur_temp = 20.

# number of degrees per minute
trate = 0.4

# duration in seconds
period = abs(target_temp - cur_temp) / (trate/60.0); 

# steps
# - lets do one for every degree
nsteps = abs(target_temp - cur_temp)

###################################################################
# Once at a safe pressure, begin cooling the device
starttim = time.time()
if (True):
    while True:
        result = vacsub.synchCommand(20,"readPressure");
        pres = result.getResult();
        print "time = %f , P = %f\n" % (time.time(),pres)
        if (pres>0.0 and pres<0.001) :
            break
        time.sleep(5.)
###################################################################

#    cryosub.synchCommand(20000,"rampTemp %f %f %d" % (period,target_temp,nsteps)).getResult()

    while (True) :
        try:
            now_temp = getrsatemp(ts8sub)
            if (cur_temp < -273.) :
                now_temp = cryosub.synchCommand(20,"getTemp B").getResult()
            if (abs(target_temp-now_temp)<0.5) :
                break
        except:
            print "unable to read temperature"
            pass
        time.sleep(10.0)
        print "waiting for target temp to be reached. current temp = %fC" % now_temp

ts5sub.synchCommand(30,"setCfgStateByName RTM")

tstart = time.time()

aa=time.ctime().split(" ")
tstart_human = (aa[4]+aa[1]+aa[2]+"-"+aa[3]).replace(":","")
fln = "%s_WarmColdMet_%s_%s_%dC.csv" % (UNITID,runnum,tstart_human,target_temp)

start_temp = {}

rsatemp = getrsatemp(ts8sub)
for temp in ["A","B","C","D"]:
    if (rsatemp > -273.) :
        start_temp[temp] = rsatemp
    else:
        start_temp[temp]=cryosub.synchCommand(20,"getTemp %s" % temp).getResult()
#    start_temp[temp]=20.0

#ts5sub.synchCommand(3000,"noStepScan  %s/Cold-Measurement.dat" % cdir)
#ts5sub.synchCommand(3000,"noStepScan  %s/%s" % (cdir,fln))
ts5sub.synchCommand(3000,"scanfl %s/%s" % (cdir,fln))

tstop = time.time()
stop_temp = {}
rsatemp = getrsatemp(ts8sub)
for temp in ["A","B","C","D"]:
    if (rsatemp>-273.) :
        stop_temp[temp] = rsatemp
    else:
        stop_temp[temp]=cryosub.synchCommand(20,"getTemp %s" % temp).getResult()
#    stop_temp[temp]=20.0

#fpdat = open("%s/Cold-Measurement.dat" % (cdir),"a");
fpdat = open("%s/%s" % (cdir,fln),"a");
fpdat.write("# start time = %f , stop time = %f\n" % (tstart,tstop))
for temp in ["A","B","C","D"]:
    fpdat.write("# temperature %s at start %f C at end %f C\n" % (temp,start_temp[temp],stop_temp[temp]))

fpdat.close()

aa=time.ctime().split(" ")
tstart_human = (aa[4]+aa[1]+aa[2]+"-"+aa[3]).replace(":","")
fpdat = open("/home/ts5prod/scans/multi-scan_%s.csv" % (tstart_human),"a");

for mcfg in ["CCD10","CCD11","CCD12","BASEPLATE","CCD10","CCD11","CCD12"] :
    aa=time.ctime().split(" ")
    tstart_human = (aa[4]+aa[1]+aa[2]+"-"+aa[3]).replace(":","")
    fln = "%s_%s.txt" % (mcfg,tstart_human)
    ts5sub.synchCommand(30,"setCfgStateByName %s" % mcfg)
    ts5sub.synchCommand(5000,"scanfl %s/%s" % (cdir,fln))
    fprdr = open("%s/%s" % (cdir,fln),"r");
    for line in fprdr :
        fpdat.write(line)
    fprdr.close()

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
