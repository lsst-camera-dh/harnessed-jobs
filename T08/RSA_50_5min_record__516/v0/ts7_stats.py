###############################################################################
# script for monitoring temperature and pressure for TS7 & 8
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

ts = "ts"

if True :
    tssub   = CCS.attachSubsystem("%s" % ts);
    cryosub = CCS.attachSubsystem("%s/Cryo" % ts );
    vqmsub  = CCS.attachSubsystem("%s/VQMonitor" % ts);
    try:
        ts8sub   = CCS.attachSubsystem("ts8");
    except:
        pass

    cdir = tsCWD

    starttim = time.time()
    fp = open("%s/ts7_stats_%d.txt" % (cdir,starttim),"w");
    for irep in range(5) :

        fp.write("\n\n ========= stats for job - %s ======== irep = %d\n" % (cdir,irep));

        result = cryosub.synchCommand(20,"getTemp","A");
        ctempa = result.getResult();
        result = cryosub.synchCommand(20,"getTemp","B");
        ctempb = result.getResult();
        result = cryosub.synchCommand(20,"getTemp","C");
        ctempc = result.getResult();
        result = cryosub.synchCommand(20,"getTemp","D");
        ctempd = result.getResult();
        result = cryosub.synchCommand(20,"getHtrRead",1);
        htr1 = result.getResult();
        result = cryosub.synchCommand(20,"getHtrRead",2);
        htr2 = result.getResult();
        result = cryosub.synchCommand(20,"getPID_P",1);
        pidp = result.getResult();
        result = cryosub.synchCommand(20,"getPID_I",1);
        pidi = result.getResult();
        result = cryosub.synchCommand(20,"getPID_D",1);
        pidd = result.getResult();
        result = cryosub.synchCommand(20,"getPID_P",2);
        pidp2 = result.getResult();
        result = cryosub.synchCommand(20,"getPID_I",2);
        pidi2 = result.getResult();
        result = cryosub.synchCommand(20,"getPID_D",2);
        pidd2 = result.getResult();
        try:
            result = vqmsub.synchCommand(10,"readPressure");
            vac=result.getResult();
        except:
            vac=-999

        rebtemp2 = {}
        rebtemp7 = {}
        ccdtemp  = {}
        rtdtemp  = {}

        for i in range(3) :
            try:
                print "Trying Reb%d"%i
                firmid      = ts8sub.synchCommand(10,"readRegister R00.Reb%d 0x1"%i).getResult()
                print "firmid = ",firmid
                rebtemp2[i] = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.Temp2"%i).getResult()
                print "rebtemp2 = ",rebtemp2[i]
                rebtemp7[i] = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.Temp7"%i).getResult()
                print "rebtemp7 = ",rebtemp7[i]
                ccdtemp[i]  = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.CCDTemp1"%i).getResult()
                print "ccdtemp = ",ccdtemp[i]
                rtdtemp[i]  = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.RTDTemp"%i).getResult()
                print "rtdtemp = ",rtdtemp[i]
            except:
                rebtemp2[i] = -999.
                rebtemp7[i] = -999.
                ccdtemp[i]  = -999.
                rtdtemp[i]  = -999.

#        fp.write("%d,%11.3e,%f,%f,%f,%f,%f,%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" % (time.time(),vac,ctempa,ctempb,ctempc,ctempd,time.time()-starttim,starttim,htr1,htr2,pidp,pidi,pidd,rebtemp2[0],rebtemp7[0],rebtemp2[1],rebtemp7[1],rebtemp2[2],rebtemp7[2],ccdtemp[0],ccdtemp[1],ccdtemp[2],rtdtemp[0],rtdtemp[1],rtdtemp[2]));
        fp.write("time = %d , vac = %11.3e Torr, ctempa = %8.2f C, ctempb = %8.2f C, ctempc = %8.2f C, ctempd = %8.2f C, htr1 = %6.1f %%, htr2 = %6.1f %%, PID_P1 = %f, PID_I1 = %f , PID_D1 = %f, PID_P2 = %f, PID_I2 = %f , PID_D2 = %f, reb0temp2 = %8.2f C, reb0temp7 = %8.2f C, reb1temp2 = %8.2f C, reb1temp7 = %8.2f C, reb2temp2 = %8.2f C, reb2temp7 = %8.2f C, ccd0temp1 = %8.2f C, ccd1temp1 = %8.2f C, ccd2temp1 = %8.2f C, rtd0temp = %8.2f C, rtd1temp = %8.2f C, rtd2temp = %8.2f C \n" % (time.time(),vac,ctempa,ctempb,ctempc,ctempd,htr1,htr2,pidp,pidi,pidd,pidp2,pidi2,pidd2,rebtemp2[0],rebtemp7[0],rebtemp2[1],rebtemp7[1],rebtemp2[2],rebtemp7[2],ccdtemp[0],ccdtemp[1],ccdtemp[2],rtdtemp[0],rtdtemp[1],rtdtemp[2]));
        time.sleep(120.)

    print "closing file"
    fp.close();

    print "ts7_stats - complete"
