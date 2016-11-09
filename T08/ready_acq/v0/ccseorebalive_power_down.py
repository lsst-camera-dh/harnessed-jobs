###############################################################################
# REB-PS safe power off
#
#
# author: homer    10/2016
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
from java.lang import RuntimeException
import sys
import time

CCS.setThrowExceptions(True);

def check_currents(rebid,pwr_chan,reb_chan,low_lim,high_lim,chkreb):

#    print "Retrieving REB PS current %s " % pwr_chan
    cur_ps = pwrsub.synchCommand(10,"getChannelValue REB%d.%s.IaftLDO" % (rebid,pwr_chan)).getResult()
#    print "Retrieving REB current %s " % reb_chan
    cur_reb = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()

#    print "verifying that the current is with limits"
    if (chkreb) :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f Amps, REB value is %8.3f Amps" % (rebname,pwr_chan,cur_ps,cur_reb)
    else :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f Amps, REB not yet ON" % (rebname,pwr_chan,cur_ps)

#    if (cur_ps < low_lim or 
    if (cur_ps> high_lim) :
        pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
        stat = "%s: Current %s with value %f mA NOT in range %f mA to %f mA. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (rebname, pwr_chan,cur_ps,low_lim,high_lim)
        raise Exception
    if (abs(cur_ps)>0.0 and chkreb) :
        if (abs(cur_reb-cur_ps)/cur_ps > 0.10 and abs(cur_reb)>0.5) :
            stat = "%s: Current %s with value %f differs by > 10%% to current from reb channel %s with value %f!" % (rebname,pwr_chan,cur_ps,reb_chan,cur_reb)
#            pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
#            stat = "%s: Current %s with value %f differs by > 20%% to current from reb channel %s with value %f. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (rebname,pwr_chan,cur_ps,reb_chan,cur_reb)
#            raise Exception(stat)

    print stat

    return

try:
    cdir = tsCWD
    unit = CCDID
    sys.stdout = open("%s/rebalive_results.txt" % cdir, "w")
    print "Running as a job harness. Results are being recorded in rebalive_results.txt"
except:
    print "Running standalone. Statements will be sent to standard output."


print "start tstamp: %f" % time.time()

if (True):
#attach CCS subsystem Devices for scripting
    ts8sub  = CCS.attachSubsystem("ts8");
    pwrsub  = CCS.attachSubsystem("ccs-rebps");
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");


    status_value = None

    result = pwrsub.synchCommand(10,"getChannelNames");
    channames = result.getResult()

#    print channames
    rebids = ts8sub.synchCommand(10,"getREBIds").getResult()

    print "setting tick and monitoring period to 0.5s"
#    ts8sub.synchCommand(10,"setTickMillis 500")

    for rebid in rebids :
            i = rebid
            rebname = 'REB%d' % i
            print "****************************************************"
            print " Starting power off procedure for %s" % rebname
            print "****************************************************"


            print "TURNING OFF REB CLOCK AND RAIL VOLTAGES"
            try:
                stat = ts8sub.synchCommand(120,"powerOff %d" % rebid).getResult()
                print stat

                print "------ %s Complete ------\n" % rebname 
            except RuntimeException, e:
                print e
            except Exception, e:
                print e

            time.sleep(2.0)

# attempt to turn off the REB power -- line by line
            print "TURNING OFF REB PS VOLTAGES"

            powers = ['od', 'heater', 'clocklo', 'clockhi', 'analog', 'digital', 'master']
            chkreb = True

            for pwr in powers :
                if 'clocklo' in pwr:
                    chkreb = False
                try:
                    print "%s: turning off %s power at %s" % (rebname,pwr,time.ctime().split()[3])
                    pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (i,pwr));
                except:
                    print "%s: failed to turn on current %s!" % (rebname,pwr)
                    throw

                time.sleep(2.0)
    
                try:
#                    print "checking currrents"
                    check_currents(i,"digital","DigI",500.,750.,chkreb)
                    check_currents(i,"analog","AnaI",400.,600.,chkreb)
                    check_currents(i,"OD","ODI",60.,120.,chkreb)
                    check_currents(i,"clockhi","ClkI",100.0,300.,chkreb)
#                   check_currents(i,"clocklo","ClkI",100.,300.,chkreb)
#                   check_currents(i,"heater","???",0.100,0.300,chkreb)
                except Exception, e:
                    print "%s: CURRENT CHECK FAILED! %s" % (rebname,e)
#                    raise Exception
                    exit
                time.sleep(2)



    print "setting tick and monitoring period to 10s"
#    ts8sub.synchCommand(10,"setTickMillis 10000")

    print "DONE"

print "stop tstamp: %f" % time.time()
