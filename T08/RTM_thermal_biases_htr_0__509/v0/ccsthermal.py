###############################################################################
#
#   - Homer
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

cdir = tsCWD


rebsub = {}
serial_number = {}
tssub  = CCS.attachSubsystem("ts");
monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
ts8sub  = CCS.attachSubsystem("%s" % ts8);
cryosub  = CCS.attachSubsystem("ts/Cryo");
pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

# set new state
istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
ext = int(jobname.split("__")[1])
if ext>400 :
    ext= ext - 400
istate = (istate & 0xffffff) | (ext << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

cdir = tsCWD

ts_version = "NA"
ts8_version = "NA"
ts_revision = "NA"
ts8_revision = "NA"

status_value = None


rebs = ""
pstep = 1
istep = 1
try:
    result = ts8sub.synchCommand(10,"getREBDevices");
    rebs = result.getResult();
    status_value = rebs
except:
    status_value = "failed"


ccdnames = {}
ccdmanunames = {}
try:
    ccdnames["00"] = CCDS00
    ccdmanunames["00"] = CCDMANUS00
    ccdnames["01"] = CCDS01
    ccdmanunames["01"] = CCDMANUS01
    ccdnames["02"] = CCDS02
    ccdmanunames["02"] = CCDMANUS02
except:
    pass
try:
    ccdnames["10"] = CCDS10
    ccdmanunames["10"] = CCDMANUS10
    ccdnames["11"] = CCDS11
    ccdmanunames["11"] = CCDMANUS11
    ccdnames["12"] = CCDS12
    ccdmanunames["12"] = CCDMANUS12
except:
    pass
try:
    ccdnames["20"] = CCDS20
    ccdmanunames["20"] = CCDMANUS20
    ccdnames["21"] = CCDS21
    ccdmanunames["21"] = CCDMANUS21
    ccdnames["22"] = CCDS22
    ccdmanunames["22"] = CCDMANUS22
except:
    pass

rafttype = "E2V"
raft = UNITID



eolib.EOTS8Setup(tssub,ts8sub,pwrsub,raft,rafttype,cdir,sequence_file,vac_outlet)

ts8sub.synchCommand(10,"setDefaultImageDirectory","%s" % (cdir));



last_cold_temp = -999.
last_cryo_temp = -999.
last_ccd_temp = -999.



ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 5000");
ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 5000");


iiter = 0
tstart = time.time()
t_lap = time.time()
seqcmnd = "setSequencerStart PseudoAcquisition"
print ts8sub.synchCommand(10,seqcmnd).getResult();

ts8sub.synchCommand(10,"setSequencerParameter ExposureTime 0")

while ((time.time()-tstart) < 3600.0) :


    ts8sub.synchCommand(10,"setTestStand","TS8")
    ts8sub.synchCommand(10,"setTestType","BIAS")


    seqcmnd = "startSequencer"
    print "seqcmnd = (%s)" % seqcmnd
    print ts8sub.synchCommand(10,seqcmnd).getResult();
    seqcmnd = "waitSequencerDone 20000"
    print "seqcmnd = (%s)" % seqcmnd

    time.sleep(2.0)



#    rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",0,False,False,"").getResult()


    if ((time.time()-t_lap) > 600.0) :
        cold_temp = cryosub.synchCommand(20,"getTemp B").getResult()
        cryo_temp = cryosub.synchCommand(20,"getTemp C").getResult()
        ccd_temp = ts8sub.synchCommand(20,"getChannelValue R00.Reb1.CCDTemp1").getResult()
    
        print "iiter = %d, delta_cold = %f, delta_cryo = %f, delta_ccd = %f" % (iiter,cold_temp-last_cold_temp,cryo_temp-last_cryo_temp,ccd_temp-last_ccd_temp)

#        if (abs(last_cold_temp-cold_temp)<0.1 and abs(last_cryo_temp-cryo_temp) < 0.1 and abs(last_ccd_temp-ccd_temp)<0.1) :
#            break

        last_cold_temp = cold_temp
        last_cryo_temp = cryo_temp
        last_ccd_temp = ccd_temp

        t_lap = time.time()

    time.sleep(0.2)
    iiter = iiter + 1

time.sleep(2.0)
ts8sub.synchCommand(10,"setTestType TS8")
ts8sub.synchCommand(10,"setImageType BIAS")
rply = ts8sub.synchCommand(100,"exposeAcquireAndSave",0,False,False,"${sensorLoc}_final_image.fits").getResult()



ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");



fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
