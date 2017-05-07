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
tssub  = CCS.attachSubsystem("ts");
monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
ts8sub  = CCS.attachSubsystem("ts8");
cryosub  = CCS.attachSubsystem("ts/Cryo");
pwrsub  = CCS.attachSubsystem("ccs-rebps");
pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

istate = tssub.synchCommand(10,"getstate").getResult()
print "istate before = ",istate," : "
istate = (istate & 0xffffff) | (int(jobname.split("__")[1]) << 24)
print "istate after = ",istate
tssub.synchCommand(10,"setstate",istate)

if (True) :

    cdir = tsCWD

    ts_version = "NA"
    ts8_version = "NA"
    ts_revision = "NA"
    ts8_revision = "NA"

    status_value = None

    wl = 500.
    for itry in range(3) :
        try:
            rwl = monosub.synchCommand(60,"setWaveAndFilter",wl).getResult();
            result = ts8sub.synchCommand(10,"setHeader","MonochromatorWavelength",rwl)
            rply = monosub.synchCommand(900,"openShutter").getResult();
            break
        except:
            time.sleep(5.0)

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

    for ii in range(10) :


        ts8sub.synchCommand(10,"setTestStand","TS8")
        ts8sub.synchCommand(10,"setTestType","DARK")

        exptime=15.0

        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",int(exptime*1000),False,False,"${sensorLoc}_${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        ts8sub.synchCommand(10,"setTestType TS8")
        ts8sub.synchCommand(10,"setImageType DARK")

        exptime=15.000

        rply = ts8sub.synchCommand(700,"exposeAcquireAndSave",int(exptime*1000),False,False,"${sensorLoc}_${sensorId}_${test_type}_${image_type}_${seq_info}_${timestamp}.fits").getResult()

        time.sleep(15.0)




fp = open("%s/status.out" % (cdir),"w");
fp.write(`istate`+"\n");
fp.close();


print "COMPLETED"
