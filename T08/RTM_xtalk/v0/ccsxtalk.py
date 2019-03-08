from org.lsst.ccs.scripting import *
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
ts8sub  = CCS.attachSubsystem("ts8");
cryosub  = CCS.attachSubsystem("ts/Cryo");
pwrsub  = CCS.attachSubsystem("rebps");
pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");
rebdevs = ts8sub.synchCommand(10,"getREBDevices").getResult()

testtype = "flat"
light = "True"
xed = "False"
exptime = 35000

ts8sub.synchCommand(10,"setTestType test")
ts8sub.synchCommand(10,"setImageType %s" % testtype)
ts8sub.synchCommand(10,"setDefaultImageDirectory","%s/S${sensorLoc}" % (cdir));


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


ss = monosub.synchCommand(10,"setSlitSize 1 2000").getResult()
ss = monosub.synchCommand(10,"setSlitSize 2 2000").getResult()
ss = monosub.synchCommand(10,"setWave 823.0").getResult()
ss = monosub.synchCommand(10,"setFilter 3").getResult()

seqcmnd = "setSequencerStart Clear"
print ts8sub.synchCommand(10,seqcmnd).getResult();
for iclear in range(0):
    seqcmnd = "startSequencer"
    print "seqcmnd = (%s)" % seqcmnd
    print ts8sub.synchCommand(10,seqcmnd).getResult();


rwl = monosub.synchCommand(10,"getWave").getResult()
ss = monosub.synchCommand(10,"getSlitSize 1").getResult()
exps = exptime / 1000.

expcmnd1 = 'exposeAcquireAndSave 0 False False ""'
expcmnd2 = "exposeAcquireAndSave %d %s %s xtalk-test-${sensorLoc}_%0.1fnm_%0.1fum_%0.1fs_${image_type}_${timestamp}.fits" % (exptime,light,xed,rwl,ss,exps)

for iclear in range(5):
    print "PRE-exposure command: expcmnd1 = ",expcmnd1
    print ts8sub.synchCommand(1500,expcmnd1).getResult()
    time.sleep(1.5) 
print "Exposure command: expcmnd2 = ",expcmnd2
for ii in range(75):
    print ts8sub.synchCommand(1500,expcmnd2).getResult() 
    time.sleep(1.5) 
    print ts8sub.synchCommand(1500,expcmnd1).getResult()
    time.sleep(1.5) 

