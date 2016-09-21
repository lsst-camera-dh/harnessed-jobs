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


def current_check():
        curmin=dict({'6V':500.0, '9V':400.0, '24V':100, '40V':60})
        curmax=dict({'6V':750.0, '9V':600.0, '24V':300, '40V':120})

    try:
        result = ts8sub.synchCommand(10,"getREBDevices");
        rebs = result.getResult();

	for rebid in rebs:
		result = pwrsub.synchCommand(10,"getChannelValue %s.digital.IaftLDO" % rebid.split('.')[0])
		curri6v = result.getResult()

		if (curri6v<curmin('6V') || curri6v>curmax('6V')) :
			throw 'Current on 6V line is %f mA which is out of range of %f -> %f mA' % (curri6v,curmin('6V'),curmax('6V'))
			cleardacs()
			clearaspics()

#	result = ts8sub.synchCommand(10,"getChannelValue %s" % (chn));


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
        pstep = 0
#ccs-rebps ccs>toggleNamedPower REB0 
#master     digital    analog     od         clockhi    clocklo    heater     dphi       hvbias     
#Error (type st for stacktrace): Error dispatching command: Error: Can't convert string 'REB0' to class int
#ccs-rebps ccs>toggleNamedPower 0 digital
#ccs-rebps ccs>toggleNamedPower 0 analog

#        pstep = pstep + 1
#        test_name = "Step%d_apply_analog_power_to_line %d" % (pstep,i)
#        try:
#            result = pwrsub.synchCommand(10,"toggleNamedPower %d analog"%i);
#            status_value = "success";
#        except:
#            status_value = "failed"
#        fp.write("%s|%s\n" % (test_name,status_value));

#  Verify data link integrity.
    rebs = ""
    pstep = pstep + 1
    test_name = "Step%d_REB_devices" % (pstep)
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
        istep = pstep + 1



        curmin=dict({'6V':500.0, '9V':400.0, '24V':100, '40V':60})
        curmax=dict({'6V':750.0, '9V':600.0, '24V':300, '40V':120})

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

# clamp the ASPICS
        print "Clamping ASPICS"
        ts8asp = [0,0,0,0,0,0,0,0]
        for i in range(6) :
            ts8asp[i] = CCS.attachSubsystem("ts8/%s.ASPIC%d" % (rebid,i))
            result = ts8asp[i].synchCommand(10,"change clamp 0xff")

        print "loading ASPICS"
        istep = istep + 1
        print "doing loadAspics"
        test_name = "Step%d_%s_load_Aspics" % (istep,rebid)
        try:
            result = ts8sub.synchCommand(10,"loadAspics true");
            status_value = result.getResult();
        except:
            print "command failure!"
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));

# #############################################################################
# record DACs and then clear them
        print "gettings configured DAC values"
        daclist = []

        ts8dacs = CCS.attachSubsystem("ts8/%s.DACS" % rebid)
        result = ts8dacs[i].synchCommand(10,"printConfigurableParameters")

        dacslist = result.getResult()

        print "setting all dacs to level 0"

# pclkHigh=700, pclkHighSh=0, pclkLow=2600, pclkLowSh=0, rgHigh=1900, rgHighSh=0, rgLow=700, rgLowSh=0, sclkHigh=1200, sclkHighSh=0, sclkLow=1600, sclkLowSh=0
        result = ts8dacs[i].synchCommand(10,"change pclkHigh 0")
        result = ts8dacs[i].synchCommand(10,"change pclkHighSh 0")
        result = ts8dacs[i].synchCommand(10,"change opclkLow 0")
        result = ts8dacs[i].synchCommand(10,"change pclkLowSh 0")
        result = ts8dacs[i].synchCommand(10,"change rgHigh 0")
        result = ts8dacs[i].synchCommand(10,"change rgHighSh 0")
        result = ts8dacs[i].synchCommand(10,"change rgLow 0")
        result = ts8dacs[i].synchCommand(10,"change rgLowSh 0")
        result = ts8dacs[i].synchCommand(10,"change sclkHigh 0")
        result = ts8dacs[i].synchCommand(10,"change sclkHighSh 0")
        result = ts8dacs[i].synchCommand(10,"change sclkLow 0")
        result = ts8dacs[i].synchCommand(10,"change sclkLowSh 0")
            
        istep = istep + 1
        print "doing loadDacs"
        test_name = "Step%d_%s_level0_load_Dacs" % (istep,rebid)
        try:
            result = ts8sub.synchCommand(10,"loadDacs true");
            status_value = result.getResult();
        except:
            print "command failure!"
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));

        print "checking current"
        current_check()

        print "turning on dacs one at a time and rechecking currents"
        for sdacs in dacslist :
            dacsname = sdacs.split('=')[0]
            dacsval  = sdacs.split('=')[1]
            print "Setting %s to %s" % (dacsname,dacsval)
            result = ts8dacs[i].synchCommand(10,"change %s %s" % (dacsname,dacsval))
            test_name = "Step%d_%s_load_Dacs_%s" % (istep,rebid,dacsname)
            try:
                result = ts8sub.synchCommand(10,"loadDacs true");
                status_value = result.getResult();
            except:
                print "command failure!"
                status_value = "failed"
            fp.write("%s|%s\n" % (test_name,status_value));

# ccs>ts8/R00.Reb0.DAC printConfigurableParameters 
#{csGate=[0,0,0], pclkHigh=700, pclkHighSh=0, pclkLow=2600, pclkLowSh=0, rgHigh=1900, rgHighSh=0, rgLow=700, rgLowSh=0, sclkHigh=1200, sclkHighSh=0, sclkLow=1600, sclkLowSh=0}

# #############################################################################
# record BIASs and then clear them
        print "gettings configured BIAS values"
        ts8bias = [0,0]
        biaslist1 = []
        biaslist2 = []
        for i in range(2) :
            ts8bias[i] = CCS.attachSubsystem("ts8/%s.BIAS%d" % (rebid,i))
            result = ts8bias[i].synchCommand(10,"printConfigurableParameters")
            if (i==0) :
                biaslist1 = result.getResult()
            if (i==1) :
                biaslist2 = result.getResult()

        print "setting all biases to level 0"
        for i in range(2) :
            result = ts8bias[i].synchCommand(10,"change gd 0")
            result = ts8bias[i].synchCommand(10,"change og 0")
            result = ts8bias[i].synchCommand(10,"change ogSh 0")
            result = ts8bias[i].synchCommand(10,"change rd 0")
            result = ts8bias[i].synchCommand(10,"change od 0")
            
        istep = istep + 1
        print "doing loadBiasDacs"
        test_name = "Step%d_%s_level0_load_BiasDacs" % (istep,rebid)
        try:
            result = ts8sub.synchCommand(10,"loadBiasDacs true");
            status_value = result.getResult();
        except:
            print "command failure!"
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));

        print "checking current"
        current_check()

        print "turning on bias dacs one at a time and rechecking currents"
        for i in range(2) :
            print "Bias%d" % i
            for sbias in biaslist :
                biasname = sbias.split('=')[0]
                biasval  = sbias.split('=')[1]
                print "Setting %s to %s" % (biasname,biasval)
                result = ts8bias[i].synchCommand(10,"change %s %s" % (biasname,biasval))
                test_name = "Step%d_%s_load_BiasDacs_%s" % (istep,rebid,biasname)
                try:
                    result = ts8sub.synchCommand(10,"loadBiasDacs true");
                    status_value = result.getResult();
                except:
                    print "command failure!"
                    status_value = "failed"
                fp.write("%s|%s\n" % (test_name,status_value));

 ccs>ts8/R00.Reb0.DAC printConfigurableParameters 
{csGate=[0,0,0], pclkHigh=700, pclkHighSh=0, pclkLow=2600, pclkLowSh=0, rgHigh=1900, rgHighSh=0, rgLow=700, rgLowSh=0, sclkHigh=1200, sclkHighSh=0, sclkLow=1600, sclkLowSh=0}




# Apply the analog power supply voltages (VP15_UNREG, VN15_UNREG, VP7_UNREG, VP40_UNREG) to the REB in the correct sequence (check with Rick for sequence and voltage values). Abort the test if any supply hits it overcurrent limit. Readback voltages and current consumption at the P/S and at the REB LTC2945 sensors.
# ccs-rafts loadNamedConfig, ccs-rafts loadDacs, ccs-rafts loadBiasDacs


        istep = istep + 1
        print "doing loadDacs"
        test_name = "Step%d_%s_load_DACS" % (istep,rebid)
        print "test_name = %s" % test_name

        try:
            print "sending loadDacs command"
            result = ts8sub.synchCommand(10,"loadDacs true");
            status_value = result.getResult();
        except:
            print "command failure!"
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

#R00.Reb2.DigV, R00.Reb2.DigI, R00.Reb2.AnaV, R00.Reb2.ClkV, R00.Reb2.ClkI, R00.Reb2.ODV, R00.Reb2.ODI, R00.Reb2.OD0V, R00.Reb2.OG0V, R00.Reb2.RD0V, R00.Reb2.GD0V, R00.Reb2.OD1V, R00.Reb2.OG1V, R00.Reb2.RD1V, R00.Reb2.GD1V, R00.Reb2.OD2V, R00.Reb2.OG2V, R00.Reb2.RD2V, R00.Reb2.GD2V, R00.Reb2.Ref05V, R00.Reb2.Ref15V, R00.Reb2.Ref25V, R00.Reb2.Ref125V,


        result = ts8sub.synchCommand(10,"getChannelNames");
        chans = result.getResult();

        istep = istep + 1
        for chn in chans :
            if rebid in chn and ("V" in chn or "I" in chn) :
                print "chn = (%s)" % chn
                test_name = "Step%d_%s_check1_VP5_LTC2945_%s" % (istep,rebid,chn)
                try:
                    result = ts8sub.synchCommand(10,"getChannelValue %s" % (chn));
                    rebval = result.getResult();

                    fp.write("%s|%f \n" % (test_name,rebval));

                except:
                    fp.write("%s| failed \n" % (test_name));




        test_name = "Step%d_%s_main_PS_current" % (istep,rebid)
        try:
            result = pwrmainsub.synchCommand(10,"getCurrent");
            status_value = result.getResult();
        except:
            status_value = "failed"
        fp.write("%s|%s\n" % (test_name,status_value));


    print "getting REB PS values"
    result = pwrsub.synchCommand(10,"getChannelNames");
    chans = result.getResult();

    print "chans = "
    print chans

    istep = istep + 1
    for ireb in range(3) :
        for chn in chans :
            print "chn = %s" % chn
            prebid = "REB%d" % ireb
            if prebid in chn and (".V" in chn or ".I" in chn) :
                print "chn = (%s)" % chn
                test_name = "Step%d_%s_check0_REB_PS_%s" % (istep,rebid,chn)
                try:
                    result = pwrsub.synchCommand(10,"getChannelValue %s" % (chn));
                    rebval = result.getResult();

                    fp.write("%s|%f \n" % (test_name,rebval));

                except:
                    fp.write("%s| failed \n" % (test_name));




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
