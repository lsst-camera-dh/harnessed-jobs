###############################################################################
# REB aliveness current_dacsloaded test
#
# Ex:
# source ts8setup-test
# [jh-test ts8prod@ts8-raft1 workdir]$ lcatr-harness --unit-type RTM --unit-id alive-test-1 --job rebalive_current_dacsloaded --version v0
#
# author: homer    5/2016
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
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");


    cdir = tsCWD

    ts_version = "NA"
    ts8_version = "NA"
    ts_revision = "NA"
    ts8_revision = "NA"

    fp = open("%s/rebalive_results.txt" % (cdir),"w");

    status_value = None

    for i in range(3) :
# attempt to apply the REB power
        pstep = 1
        test_name = "Step%d_power_to_line %d" % (pstep,i)
        try:
            result = pwrsub.synchCommand(10,"setPowerOn",i,-1,True);
            status_value = "success";
        except:
            status_value = "failed"
            fp.write("%s|%s\n" % (test_name,status_value));

#  Verify data link integrity.
    rebs = ""
    pstep = pstep + 1
    test_name = "Step%d_%s_REB_devices" % (pstep,i)
    try:
        result = ts8sub.synchCommand(10,"getREBDevices");
        rebs = result.getResult();
        status_value = rebs
    except:
        status_value = "failed"
    fp.write("%s| %s\n" % (test_name,status_value));

    for rebid in rebs :
#        fp.write("\n\nREB ID = %s\n" % rebid)
#        fp.write("==============================\n")
# Read 1-wire ID chip and record the value.
        istep = pstep + 1
        test_name = "Step%d_%s_1-wire_ID" % (istep,rebid)
        try:
# SCI's own address
            result = ts8sub.synchCommand(10,"readRegister "+rebid+" 1");
            sci_id = result.getResult();
            status_value = sci_id
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));

# Read and record the REB firmware version.
# see: https://confluence.slac.stanford.edu/display/LSSTCAM/REB+Register+Sets
        istep = istep + 1
        test_name = "Step%d_%s_REB_firmware_version" % (istep,rebid)
        try:
            result = ts8sub.synchCommand(10,"readRegister "+rebid+" 0");
            firmver = result.getResult();
            status_value = firmver
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));


# record all DAC parameters
        istep = istep + 1
        test_name = "Step%d_%s_DAC_parameters" % (istep,rebid)
        ts8dac = CCS.attachSubsystem("ts8/%s.DAC" % (rebid))
        try:
            cmnd = "printConfigurableParameters"
            result = ts8dac.synchCommand(10,cmnd);
            rdac = result.getResult();
            print "DAC parameters\n%s" % rdac
            rdacstr = "%s" % rdac
            for line in rdacstr.strip("{|}").split(",") :
                print "test_name = %s" % test_name
                print "line = %s" % line
                vals = line.strip("[|]").split("=")
                fp.write("%s_%s| %s \n" % (test_name,vals[0],vals[1].strip("[|]")));
        except:
            fp.write("%s| failed \n" % (test_name));

        ts8asp = [0,0,0,0,0,0,0,0]
        for i in range(6) :
            ts8asp[i] = CCS.attachSubsystem("ts8/%s.ASPIC%d" % (rebid,i))

        for iasp in range(6) :
            test_name = "Step%d_%s_DAC_parms_ASPIC%d" % (istep,rebid,iasp)
            try:
                cmnd = "printConfigurableParameters"
                result = ts8asp[iasp].synchCommand(10,cmnd);
                rasp = "%s" % result.getResult();
                print "DAC parms ASPIC%d \n %s" % (iasp,rasp)
                for line in rasp.strip("{|}").split(",") :
                    print "test_name = %s" % test_name
                    print "line = %s" % line
                    vals = line.split("=")
                    fp.write("%s_%s| %s \n" % (test_name,vals[0].strip(" "),vals[1]));
            except:
                fp.write("%s| failed \n" % (test_name));

# Read the voltage and current consumption measured by the VP5 LTC2945 current monitor on the REB, record the value and compare to the current measured at the P/S.

        chans = ["6V","9V","24V","40V"]
        curmin=dict({'6V':500.0, '9V':400.0, '24V':100, '40V':60}) 
        curmax=dict({'6V':750.0, '9V':600.0, '24V':300, '40V':120}) 

        istep = istep + 1
        for chn in chans :
            test_name = "Step%d_%s_check0_VP5_LTC2945_%s" % (istep,rebid,chn)
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%s_rebv|%f \n" % (test_name,rebv));
                fp.write("%s_rebi|%f \n" % (test_name,rebi));
                fp.write("%s_rebi_min|%f \n" % (test_name,curmin[chn]/1.e6));
                fp.write("%s_rebi_max|%f \n" % (test_name,curmax[chn]/1.e6));
            except:
                fp.write("%s| failed \n" % (test_name));


# Apply the analog power supply voltages (VP15_UNREG, VN15_UNREG, VP7_UNREG, VP40_UNREG) to the REB in the correct sequence (check with Rick for sequence and voltage values). Abort the test if any supply hits it overcurrent limit. Readback voltages and current consumption at the P/S and at the REB LTC2945 sensors.
# ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs
        istep = istep + 1
        test_name = "Step%d_%s_load_Dacs_power" % (istep,rebid)
        try:
            result = pwrsub.synchCommand(10,"loadDacs",true);
            status_value = "success";
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));


        istep = istep + 1
        test_name = "Step%d_%s_load_BiasDacs_power" % (istep,rebid)
        try:
            result = pwrsub.synchCommand(10,"loadBiasDacs",true);
            status_value = "success";
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));
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

        istep = istep + 1
        for chn in chans :
            test_name = "Step%d_%s_check1_VP5_LTC2945_%s" % (istep,rebid,chn)
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%s_rebv|%f \n" % (test_name,rebv));
                fp.write("%s_rebi|%f \n" % (test_name,rebi));
                fp.write("%s_rebi_min|%f \n" % (test_name,curmin[chn]/1.e6));
                fp.write("%s_rebi_max|%f \n" % (test_name,curmax[chn]/1.e6));
            except:
                fp.write("%s| failed \n" % (test_name));




        test_name = "Step%d_%s_main_PS_current" % (istep,rebid)
        try:
            result = pwrmainsub.synchCommand(10,"getCurrent");
            status_value = result.getResult();
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));



# Readback the temperatures measured by each of the ADT7420 sensors on the REB.

        istep = istep + 1
        for itemp in range(1,9) :
            test_name = "Step%d_%s_REB_Temp_%s" % (istep,rebid,itemp)
            try:
                cmnd = "getChannelValue %s.Temp%d" % (rebid,itemp)
                print "temperature read command=%s" % cmnd
                result = ts8sub.synchCommand(10,cmnd);
                rebt = result.getResult();
                fp.write("%s|%f \n" % (test_name,rebt));
            except:
                fp.write("%s| failed \n" % (test_name));

        for itemp in range(1,3) :
            test_name = "Step%d_%s_DREB_Temp_%s" % (istep,rebid,itemp)
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.Temp%d" % (rebid,itemp));
                rebt = result.getResult();
                fp.write("%s|%f \n" % (test_name,rebt));
            except:
                fp.write("%s| failed \n" % (test_name));

# Apply the CCD bias voltages and set the CCD clock rails (to E2V levels).
        result = ts8sub.synchCommand(90,"loadSequencer","seq_1M.xml");

#ccs-rebps/setBiasDac ?  ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs

#12. Re-check supply currents and verify they do not exceed expected values.

        istep = istep + 1
        for chn in chans :
            test_name = "Step%d_%s_check2_VP5_LTC2945_%s" % (istep,rebid,chn)
            try:
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%sv" % (rebid,chn));
                rebv = result.getResult();
                result = ts8sub.synchCommand(10,"getChannelValue D%s.%si" % (rebid,chn));
                rebi  = result.getResult();
                fp.write("%s_rebv|%f \n" % (test_name,rebv));
                fp.write("%s_rebi|%f \n" % (test_name,rebi));
                fp.write("%s_rebi_min|%f \n" % (test_name,curmin[chn]/1.e6));
                fp.write("%s_rebi_max|%f \n" % (test_name,curmax[chn]/1.e6));
            except:
                fp.write("%s| failed \n" % (test_name));


#13. Configure the ASPICs to standard gain and RC time constant, and leave the inputs in clamped state.

        for i in range(6) :
            ts8asp[i].synchCommand(10,"change clamp 1");


#14. Execute a zero-second exposure and readout sequence. Start a timer when the close shutter command executes.
 
        ts8sub.synchCommand(10,"setHeader","TestType","LAMBDA",False)
        ts8sub.synchCommand(10,"setHeader","ImageType","BIAS",False)
        ts8sub.synchCommand(10,"setFitsFilesOutputDirectory","%s" % (cdir));

# <LSST CCD SN>_<test type>_<image type>_<seq. info>_<time stamp>.fits
        fitsfilename = "%s_lambda_bias_%4.4d_%3.3d_%s.fits" % (rebid,0,0,time.time())
        print "fitsfilename = %s" % fitsfilename
        
        tm_start = time.time()
        print "Ready to take image with exptime = %f at time = %f" % (0,tm_start)
        
        result = ts8sub.synchCommand(500,"exposeAcquireAndSave",0,False,False,fitsfilename);
        something = result.getResult();
        tm_end = time.time()
        print "done taking image with exptime = %f at time = %f" % (0,tm_end)
        
        istep = istep + 1
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_start" % (istep,rebid),tm_start));
        fp.write("%s| %s \n" % ("Step%d_%s_bias_exposure_t_end" % (istep,rebid),tm_end));


    fp.close();

# satisfy the expectations of ccsTools
    istate=0;
    fp = open("%s/status.out" % (cdir),"w");
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % ts8_version);
    fp.write("%s\n" % ts8_revision);
    fp.close();


print "rebalive_functionalty test END"


###############################################################################               
# EOgetCCSVersions: getCCSVersions                                                            
def TS8getCCSVersions(ts8sub,cdir):
    result = ts8sub.synchCommand(10,"getCCSVersions");
    ccsversions = result.getResult()
    ccsvfiles = open("%s/ccsversion" % cdir,"w");
    ccsvfiles.write("%s" % ccsversions)
    ccsvfiles.close()

    ssys = ""

    ts8_version = ""
    ccsrebps_version = ""
    ts8_revision = ""
    ccsrebps_revision = ""
    for line in str(ccsversions).split("\t"):
        tokens = line.split()
        if (len(tokens)>2) :
            if ("ts8" in tokens[2]) :
                ssys = "ts8"
            if ("ccs-rebps" in tokens[2]) :
                ssys = "ccs-rebps"
            if (tokens[1] == "Version:") :
                print "%s - version = %s" % (ssys,tokens[2])
                if (ssys == "ts8") :
                    ts8_version = tokens[2]
                if (ssys == "ccs-rebps") :
                    ccsrebps_version = tokens[2]
            if (len(tokens)>3) :
                if (tokens[2] == "Rev:") :
                    print "%s - revision = %s" % (ssys,tokens[3])
                    if (ssys == "ts8") :
                        ts8_revision = tokens[3]
                    if (ssys == "ccs-rebps") :
                        ccsrebps_revision = tokens[3]

    return(ts8_version,ccsrebps_version,ts8_revision,ccsrebps_revision)
