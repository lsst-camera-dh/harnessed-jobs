###############################################################################
# REB-PS safe power on
#
#
# author: homer    10/2016
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
import sys
import time

CCS.setThrowExceptions(True);

def check_currents(rebid,pwr_chan,reb_chan,low_lim,high_lim,chkreb):

#    print "Retrieving REB PS current %s " % pwr_chan
    cur_ps = pwrsub.synchCommand(10,"getChannelValue REB%d.%s.IaftLDO" % (rebid,pwr_chan)).getResult()
#    print "Retrieving REB current %s " % reb_chan
    cur_reb = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()

#    print "verifying that the current is with limits"
    stat = "%10.10s : OK - PS value is %8.3f , REB value is %8.3f" % (pwr_chan,cur_ps,cur_reb)
#    if (cur_ps < low_lim or 
    if (cur_ps> high_lim) :
        pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
        stat = "Current %s with value %f mA NOT in range %f mA to %f mA. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (pwr_chan,cur_ps,low_lim,high_lim)
        raise Exception
    if (abs(cur_ps)>0.0 and chkreb) :
        if (abs(cur_reb-cur_ps)/cur_ps > 0.20) :
            pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
            stat = "Current %s with value %f differs by > 10%% to current from reb channel %s with value %f. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (pwr_chan,cur_ps,reb_chan,cur_reb)
            raise Exception(stat)

    print stat

    return



if (True):
#attach CCS subsystem Devices for scripting
    ts8sub  = CCS.attachSubsystem("ts8");
    pwrsub  = CCS.attachSubsystem("rebps");
    pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");


    status_value = None

    result = pwrsub.synchCommand(10,"getChannelNames");
    channames = result.getResult()

#    print channames
    rebids = ts8sub.synchCommand(10,"getREBIds").getResult()

    for i in rebids :
#        print "Checking if REBID=%d is present" % i
#        present = False
#        for ch in channames:
#            if "REB%d" % i in ch:
#                present = True

#        if present :
#            print "Checking REBID=%d : " % i


# verify that all power is OFF
            try:
#                result = pwrsub.synchCommand(10,"setNamedPowerOn",i,"master",False);
                result = pwrsub.synchCommand(10,"setNamedPowerOn %d master False" % i);
            except Exception, e:
#                print "REB with id %d  appears not to be present - SKIPPING" % i
#                continue
                print "FAILED TO TURN POWER OFF! %s" % e
                raise Exception

            time.sleep(2.0)

# attempt to apply the REB power -- line by line
            powers = ['master', 'digital', 'analog', 'clockhi', 'clocklo', 'heater', 'od']
            chkreb = False

            for pwr in powers :
                if 'heat' in pwr:
                    chkreb = True
                try:
                    print "turning on %s power" % pwr
                    pwrsub.synchCommand(10,"setNamedPowerOn %d %s True" % (i,pwr));
                except:
                    print "failed to turn on current %s!" % pwr
                    throw

                time.sleep(2.0)
    
                try:
#                    print "checking currrents"
                    check_currents(i,"digital","DigI",500.,750.,chkreb)
                    check_currents(i,"analog","AnaI",400.,600.,chkreb)
                    check_currents(i,"OD","ODI",60.,120.,chkreb)
                    check_currents(i,"clockhi","ClkI",100.0,300.,chkreb)
#                    check_currents(i,"clocklo","ClkI",100.,300.,chkreb)
#                check_currents(i,"heater","???",0.100,0.300,chkreb)
                except Exception, e:
                    print "CURRENT CHECK FAILED! %s" % e
                    raise Exception
                time.sleep(2)

    print "PROCEED TO TURN ON REB CLOCK AND RAIL VOLTAGES"
    stat = ts8sub.synchCommand(120,"powerOn").getResult()
    print stat

    print "DONE"


