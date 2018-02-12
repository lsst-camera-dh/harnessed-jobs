###############################################################################
# fe55
# Acquire fe55 image pairs
#
###############################################################################
from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import traceback
import eolib

CCS.setThrowExceptions(True)

try:
    #attach CCS subsystem Devices for scripting
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts)
    print "attaching Bias subsystem"
    biassub   = CCS.attachSubsystem("%s/Bias" % ts)
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts)
#    print "attaching XED subsystem"
#    xedsub   = CCS.attachSubsystem("%s/Fe55" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts )
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts )
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon)

    time.sleep(3.)

    cdir = tsCWD


    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)
except:
    print "pre-setup problem!"
    traceback.print_exc()

eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)


try:

    print "set controller parameters for an exposure with the shutter closed"
    arcsub.synchCommand(10,"setParameter","Light","0")
    arcsub.synchCommand(10,"setParameter","Fe55","0")

#    arcsub.synchCommand(10,"setDefaultCCDTypeName","BNLITL")

    ccd = CCDID
    print "Working on CCD %s" % ccd

# clear the buffers
    print "doing some unrecorded bias acquisitions to clear the buffers"
    print "set controller for bias exposure"
    arcsub.synchCommand(10, "setParameter", "Fe55", "0")
    arcsub.synchCommand(10, "setParameter", "Light", "0")
    arcsub.synchCommand(10, "setParameter", "ExpTime", "0")
    for i in range(5):
        timestamp = time.time()
        result = arcsub.synchCommand(10, "setFitsFilename", "")
        print "Ready to take clearing bias image. time = %f" % time.time()
        result = arcsub.synchCommand(20, "exposeAcquireAndSave")
        rply = result.getResult()
        result = arcsub.synchCommand(500, "waitForExpoEnd")
        rply = result.getResult()

    arcsub.synchCommand(10, "setFitsDirectory", "%s" % cdir)
    arcsub.synchCommand(10, "setRawSampleFileName", "%s_rawsample_%%{rawsel}_%%{TIMESTAMP}.txt" % ccd)
    print "start raw sample acquisition"
    for i in range(16):
        arcsub.synchCommand(10, "setRawSel", str(i))
        arcsub.synchCommand(100, "powerOnCCD")
        result = arcsub.synchCommand(100, "exposeAcquireRawSample")
        rply = result.getResult()
        result = arcsub.synchCommand(500, "waitForExpoEnd")
        rply = result.getResult()

except Exception, ex:
    traceback.print_exc()
    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "Raw sample acquisition has finished"
