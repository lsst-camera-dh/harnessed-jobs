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


#  try to power ON rebs using the safepowerON method
    rebs = ""
    pstep = pstep + 1
    test_name = "Step%d_REB_devices" % (pstep)
    try:
        result = ts8sub.synchCommand(10,"safePowerOn");
        rebsOn = result.getResult();
        status_value = rebsOn
    except:
        status_value = "failed"
    fp.write("%s| %s\n" % (test_name,status_value));


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
