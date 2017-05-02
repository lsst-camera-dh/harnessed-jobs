###############################################################################
# pressure_check
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

if (True) :
#attach CCS subsystem Devices for scripting
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "attaching VQM subsystem"
    vqmsub = CCS.attachSubsystem("%s/VQMonitor" % ts );

    time.sleep(3.)

    cdir = tsCWD




    vac_outlet = 12
    pres  = 99999.
    try:
        print "checking current pressure"
        press = vqmsub.synchCommand(30,"readPressure").getResult();
    except:
        pass
    print "press = ",press
    if (False) :
        if (press > 900. or press is 0.0 or press < 0.0) :
            print "turning VQM ON"
            reply = pdusub.synchCommand(360,"ts/PDU setOutletState %d true" % vac_outlet).getResult();
        print "sleeping for 3 mins"
        time.sleep(180)
        print "ready to turn VQM off"
        try:
            reply = tssub.synchCommand(30,"disconnectVQM").getResult();
        except:
            print "failed to disconnect from VQM"
            pass
        print "turning VQM off"
        reply = pdusub.synchCommand(360,"ts/PDU setOutletState %d false" % vac_outlet).getResult();
    print "done"

    ts_version = -1
    ts_revision = -1
    ts8_version = -1
    ts8_revision = -1

    fp = open("%s/status.out" % (cdir),"w");
    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.close();


print "pressure_check: COMPLETED"
