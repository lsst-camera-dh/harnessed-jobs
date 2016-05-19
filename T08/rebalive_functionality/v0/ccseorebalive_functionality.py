###############################################################################
# REB aliveness functionality test
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

if (True):
#attach CCS subsystem Devices for scripting
    ts8sub  = CCS.attachSubsystem("ts8");
    pwrsub  = CCS.attachSubsystem("ccs-rebps");
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainPS");

    for i in range(5) :
        ts8asp%i = CCS.attachSubsystem("ts8/R00.Reb2.ASPIC%d" % i)

    time.sleep(3.)

    cdir = tsCWD

    ts_version = ""
    ts8_version = ""
    ts_revision = ""
    ts8_revision = ""

    fp = open("%s/rebalive_report.results" % (cdir),"w");

# attempt to power apply the REB power
    test_name = "apply_power"
    try:
        result = pwrsub.synchCommand(10,"togglePower");
        status_value = "success";
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value));

#  Verify data link integrity.
    rebs = ""
    test_name = "link_integrity"
    try:
        result = ts8sub.synchCommand(10,"getREBDevices");
        rebs = result.getResult();
        status_values = rebs
    except:
        status_value = "failed"
    fp.write("%-20s\t | \t %s\n" % (test_name,status_value));

    for rebid in rebs :
        print "REB ID = %s" % rebid
        print "=============================="
# Read 1-wire ID chip and record the value.
        test_name = "link_integrity"
        try:
# SCI's own address
            result = ts8sub.synchCommand(10,"readRegister "+rebid+" 2");
            fitsfilename = result.getResult();
            status_value = "success"
        except:
            status_value = "failed"
        fp.write("%-20s\t | \t %s\n" % (test_name,status_value));

# Read and record the REB firmware version.
# see: https://confluence.slac.stanford.edu/display/LSSTCAM/REB+Register+Sets
        test_name = "REB_firmware_version"
        try:
            result = ts8sub.synchCommand(10,"readRegister "+rebid+" 0");
            fitsfilename = result.getResult();
            status_value = "success"
        except:
            status_value = "failed"
        fp.write("%-20s\t | \t %s\n" % (test_name,status_value));


# Read the voltage and current consumption measured by the VP5 LTC2945 current monitor on the REB, record the value and compare to the current measured at the P/S.
        chans = [6V 9V 24V 40V]

        for chn in chans :
            test_name = "VP5_LTC2945_%s" % chn
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv =  = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%-20s\t | \t %f \t %f  | \t %f \t %f \n" % (test_name,rebv, rebi, curmin[chn],curmax[chn]));
            except:
                fp.write("%-20s\t | failed | failed \n" % (test_name));


# Apply the analog power supply voltages (VP15_UNREG, VN15_UNREG, VP7_UNREG, VP40_UNREG) to the REB in the correct sequence (check with Rick for sequence and voltage values). Abort the test if any supply hits it overcurrent limit. Readback voltages and current consumption at the P/S and at the REB LTC2945 sensors.
# ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs
        test_name = "apply analog power"
        try:
            result = pwrsub.synchCommand(10,"loadDacs",true);
            status_value = "success";
        except:
            status_value = "failed"
        fp.write("%-20s\t | \t %s\n" % (test_name,status_value));



        test_name = "apply analog power"
        try:
            result = pwrsub.synchCommand(10,"loadBiasDacs",true);
            status_value = "success";
        except:
            status_value = "failed"
        fp.write("%-20s\t | \t %s\n" % (test_name,status_value));
#
# 
#

# Verify that all currents are within the expected range 

# Record the value of the currents on each supply, both at the P/S and by the REB.

# REB4 Supply current expected ranges (voltage, current min, current max) [mA]
#+5V	500	750
#+7V	400	600
#+15V	100	300
#+40V	60	120
# Note: -15V monitor is not operational on REB4.
        curmin=dict({'6V':500.0, '9V':400.0, '24V':100, '40V':60}) 
        curmax=dict({'6V':750.0, '9V':600.0, '24V':300, '40V':120}) 

        for chn in chans :
            test_name = "VP5_LTC2945_%s" % chn
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv =  = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%-20s\t | \t %f \t %f  | \t %f \t %f \n" % (test_name,rebv, rebi, curmin[chn],curmax[chn]));
            except:
                fp.write("%-20s\t | failed | failed \n" % (test_name));




        test_name = "main PS current"
        try:
            result = pwrmainsub.synchCommand(10,"getCurrent",true);
            status_value = "success";
        except:
            status_value = "failed"
        fp.write("%-20s\t | \t %s\n" % (test_name,status_value));




# Readback the temperatures measured by each of the ADT7420 sensors on the REB.

        for itemp in range(1,5) :
            test_name = "Temp_%s" % itemp
            try:
                result = ts8sub.synchCommand(10,"getChannelValue %s.%d" % (rebid,itemp));
                rebt =  = result.getResult();
                fp.write("%-20s\t | \t %f \t %f  | \t %f \t %f \n" % (test_name,rebt));
            except:
                fp.write("%-20s\t | failed | failed \n" % (test_name));

# Apply the CCD bias voltages and set the CCD clock rails (to E2V levels).
        result = ts8sub.synchCommand(90,"loadSequencer","seq_1M.xml");

#ccs-rebps/setBiasDac ?  ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs

#12. Re-check supply currents and verify they do not exceed expected values.

        for chn in chans :
            test_name = "VP5_LTC2945_%s" % chn
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv =  = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%-20s\t | \t %f \t %f  | \t %f \t %f \n" % (test_name,rebv, rebi, curmin[chn],curmax[chn]));
            except:
                fp.write("%-20s\t | failed | failed \n" % (test_name_));


#13. Configure the ASPICs to standard gain and RC time constant, and leave the inputs in clamped state.

         for i in range(5) :
             ts8asp%i.synchCommand(10,"change clamp 1");


#14. Execute a zero-second exposure and readout sequence. Start a timer when the close shutter command executes.
 
         ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA",False)
         ts8sub.synchCommand(10,"setHeader","ImageType","BIAS",False)
         ts8sub.synchCommand(10,"setExposureParameter exposure_time 0");
         ts8sub.synchCommand(10,"setExposureParameter open_shutter false");
         ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));

         fitsfilename = "%s_lambda_flat_%4.4d_%3.3d_%s.fits" % (raft,int(wl),seq,time.time())
         ts8sub.synchCommand(10,"setFitsFilesNamePattern",fitsfilename);
         print "fitsfilename = %s" % fitsfilename

         tm_start = time.time()
         print "Ready to take image with exptime = %f at time = %f" % (0,tm)
       
         result = ts8sub.synchCommand(500,"exposeAcquireAndSave");
         something = result.getResult();
         tm_end = time.time()

         fp.write("bias image\t | %s | %s \n" % (tm_start, tm_end);


     fp.close();



print "rebalive_functionalty test END"
