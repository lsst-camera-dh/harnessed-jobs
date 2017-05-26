######################################################################
#    Collect data to measure power ratio between RSA and REBs
#       - Homer    20170515
# usage:
# [jh]$ ShellCommandConsole | tee logts8rsapwr_1
#  executeScript /home/ts8prod/workdir/ts8rsatest.py
######################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

ts8sub  = CCS.attachSubsystem("ts8");
pwrsub = CCS.attachSubsystem("ccs-rebps")
testtype = "FE55"
light = "False"
xed = "True"
exptime = 16000
idx = 0

print "temp control active - ",ts8sub.synchCommand(10,"isTempControlActive").getResult()
print "time = ",time.time()
print "rsa heater power = ",ts8sub.synchCommand(10,"getChannelValue R00.Reb0.HtrW").getResult()
for ireb in range(3) :
    print "reb %d total power at PS" % ireb,pwrsub.synchCommand(10,"getChannelValue REB%d.Power" % ireb).getResult()

ts8sub.synchCommand(10,"setTestType test")
ts8sub.synchCommand(10,"setImageType %s" % testtype)
ts8sub.synchCommand(10,"setDefaultImageDirectory /home/ts8prod/workdir/rsa_htr_power_test_%s/" % int(time.time()))

expcmnd1 = 'exposeAcquireAndSave 0 False False ""'

expcmnd2 = "exposeAcquireAndSave %d %s %s ts8rsatest-${sensorLoc}_r${raftLoc}_${test_type}_${image_type}_${timestamp}.fits" % (exptime,light,xed)

for iclear in range(2):
    print "PRE-exposure command: expcmnd1 = ",expcmnd1
    print ts8sub.synchCommand(1500,expcmnd1).getResult()
    time.sleep(0.5) 


for i in range(30) :
    print "exposure index ",i
    print "Exposure command: expcmnd2 = ",expcmnd2
    print ts8sub.synchCommand(1500,expcmnd2).getResult() 
    print "time = ",time.time()
    print "rsa heater power = ",ts8sub.synchCommand(10,"getChannelValue R00.Reb0.HtrW").getResult()
    for ireb in range(3) :
        print "reb %d total power at PS" % ireb,pwrsub.synchCommand(10,"getChannelValue REB%d.Power" % ireb).getResult()



for i in range(30) :
    print "Now sleeping 10 minutes while operator powers down back/front biases and clocks"

time.sleep(600.0)

for i in range(60) :
    print "time = ",time.time()
    print "rsa heater power = ",ts8sub.synchCommand(10,"getChannelValue R00.Reb0.HtrW").getResult()
    for ireb in range(3) :
        print "reb %d total power at PS" % ireb,pwrsub.synchCommand(10,"getChannelValue REB%d.Power" % ireb).getResult()
    time.sleep(60.0)

