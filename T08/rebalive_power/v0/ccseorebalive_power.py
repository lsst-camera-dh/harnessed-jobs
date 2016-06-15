###############################################################################
# REB aliveness power test
#
# Ex:
# source ts8setup-test
# [jh-test ts8prod@ts8-raft1 workdir]$ lcatr-harness --unit-type RTM --unit-id alive-test-1 --job rebalive_power_to_line --version v0
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

    rebs = ""
    pstep = 1
    istep = 1
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
