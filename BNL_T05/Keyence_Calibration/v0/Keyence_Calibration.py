###############################################################################
# metro_acq
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

ts5sub.synchCommand(30,"setCfgStateByName RTM-calib")

tstart = time.time()
start_temp = {}
for temp in ["A","B","C","D"]:
    start_temp.append(cryosub.synchCommand(20,"getTemp %s" % temp).getResult())

ts5sub.synchCommand(3000,"noStepScan  %s/RSA-calib.dat" % cdir)

tstop = time.time()
stop_temp = {}
for temp in ["A","B","C","D"]:
    stop_temp.append(cryosub.synchCommand(20,"getTemp %s" % temp).getResult())

fpdat = open("%s/RSA-calib.dat" % (cdir),"a");
fpdat.write("start time = %f , stop time = %f\n" % (tstart,tstop))
for temp in ["A","B","C","D"]:
    fpdat.write("temperature %s at start %f C at end %f C\n" % (temp,start_temp[idx],stop_temp[idx]))

fpdat.close()


fpdat = open("%s/RSA-calib.dat" % (cdir),"r");

calibOK = True
for line in fpdat:
    if ("-999." in line) :
        calibOK = False
fpdat.close()

if calibOK :

    print "calibration check successful"

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

else :

    print "calibration check FAILED!"

    raise Exception("calibration check FAILED") 

print " =====================================================\n"
print "            TS5 KEYENCE METROLOGY SCAN DONE\n"
print " =====================================================\n"


print "Keyence_Calobration: COMPLETED"
