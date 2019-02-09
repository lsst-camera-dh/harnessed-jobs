#!/usr/bin/env ccs-script                                                                                                           
from optparse import OptionParser
from org.lsst.ccs.scripting import CCS
import os
#from ccs import aliases
import time
#from ccs import proxies

ts8 = os.getenv("CCS_TS8")
raftid = "R00"

#fp = CCS.attachProxy(ts8)
#fpr22 = CCS.attachSubsystem("%s/%s" % (ts8,raftid))
fp = CCS.attachSubsystem("%s" % (ts8))

#CCS.setDefaultTimeout(30)


for rebname in fp.sendSynchCommand("getREBDeviceNames") :
    print "========================================================"
    print "Checking %s at %s" % (rebname,time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime()))
    fpreb = CCS.attachSubsystem("%s/%s" % (ts8,rebname))
    print "%s firmware version = " % rebname , fpreb.sendSynchCommand("getHwVersion")
    print "%s serial number = " % rebname , fpreb.sendSynchCommand("getSerialNumber")


    for ch in fp.sendSynchCommand("getChannelNames"):
        if rebname in ch :
            print ch, fp.sendSynchCommand("getChannelValue %s" % ch)
    print "========================================================\n\n"
#print fpr22.sendSynchCommand("getREBHwVersions")
#print fpr22.sendSynchCommand("getREBSerialNumbers")
