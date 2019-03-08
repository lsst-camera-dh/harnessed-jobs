###############################################################################
# REB-PS safe power on
#
#
# author: homer    8/2017
#
###############################################################################

from org.lsst.ccs.scripting import CCS
from java.lang import Exception
from java.lang import RuntimeException
import sys
import time
import subprocess



CCS.setThrowExceptions(True);

#################################################################
#   Check that PS current levels are within acceptable range
#################################################################
def check_currents(rebid,pwr_chan,reb_chan,low_lim,high_lim,chkreb):

    print "Retrieving REB PS current %s " % pwr_chan
    cur_ps = pwrsub.synchCommand(10,"getChannelValue REB%d.%s.IaftLDO" % (rebid,pwr_chan)).getResult()
    print "Retrieving REB current %s " % reb_chan
    cur_reb = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()

    print "verifying that the current is within limits"
    if (chkreb) :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f mAmps, REB value is %8.3f mAmps" % (rebname,pwr_chan,cur_ps,cur_reb)
    else :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f mAmps, REB not yet ON" % (rebname,pwr_chan,cur_ps)

        print " ... stat = ",stat
    if (cur_ps < low_lim or cur_ps> high_lim) :
        pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
        stat = "%s: Current %s with value %f mA NOT in range %f mA to %f mA. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (rebname, pwr_chan,cur_ps,low_lim,high_lim)
        raise Exception(stat)
    if (abs(cur_ps)>0.0 and chkreb) :
        if (abs(cur_reb-cur_ps)/cur_ps > 0.10 and abs(cur_reb)>0.5) :
            stat = "%s: Current %s with value %f differs by > 10%% to current from reb channel %s with value %f!" % (rebname,pwr_chan,cur_ps,reb_chan,cur_reb)

    print stat

    return


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("%s/rebalive_results.txt" % tsCWD, "a")

    def write(self, message):
        self.terminal.write(message+"\r")
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    


######################################################################################
########################      MAIN             #######################################
########################          MAIN         #######################################
######################################################################################

dorun = True

# The following will cause an exception if not run as part of a harnessed job because
# tsCWD and CCDID will not be defined in that case
try:
    cdir = tsCWD
    unit = CCDID

    sys.stdout = Logger()
    print "Running as a job harness. Results are being recorded in rebalive_results.txt"
except:
    print "Running standalone. Statements will be sent to standard output."


print "start tstamp: %f" % time.time()

if not dorun :
    print "setup for repair ... not running"
else :
#attach CCS subsystem Devices for scripting
    ts8sub  = CCS.attachSubsystem("ts8");
    pwrsub  = CCS.attachSubsystem("rebps");
    pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");


    status_value = True

    result = pwrsub.synchCommand(10,"getChannelNames");
    channames = result.getResult()


    rebids = ts8sub.synchCommand(10,"getREBIds").getResult()

    idmap = []

    print "length = %d" % len(sys.argv)
    print str(sys.argv)

    for arg in sys.argv :
        if ":" in arg :
            idmap.append(arg)

# check for one by one connectivity jobs
    if "connectivity0" in jobname :
        idmap.append("0:0")
    if "connectivity1" in jobname :
        idmap.append("1:1")
    if "connectivity2" in jobname :
        idmap.append("2:2")

# if nothing specified ... do it all
    if (len(idmap)==0) :
        for rebid in rebids :
            print "rebid = %s" % rebid
            idmap.append("%d:%d" % (int(rebid),int(rebid)))

    print "Will attempt to power on:"
    for ids in idmap :
        pwrid = int(ids.split(":")[0])
        rebid = int(ids.split(":")[1])
        print "power line %d for REB ID %d" % (pwrid,rebid)


    print "setting tick and monitoring period to 0.5s"

    for ids in idmap :
        pwrid = int(ids.split(":")[0])
        rebid = int(ids.split(":")[1])

        if status_value :
            i = pwrid
            rebname = 'REB%d' % i
            print "****************************************************"
            print " Starting power ON procedure for REB power line %s and REB %s" % (pwrid,rebname)
            print "****************************************************"


# Insure the front and back biases are off and increase the monitoring update rate
            ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 500");
            ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 500");

            stat = ts8sub.synchCommand(300,"R00.Reb%d setBackBias false" % rebid).getResult()
            
            try:
                stat = ts8sub.synchCommand(300,"powerOff %d" % rebid).getResult()
            except Exception, e:
                print "%s: FAILED TO TURN POWER OFF! \r\r %s" % (rebname,e)
                ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
                ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");
                raise e

            time.sleep(3.0)

            pwron = ""
# Turn on the REB PS power lines but keep off the RSA heaters

            try:
                print "%s: turning on %s power at %s" % (rebname,pwr,time.ctime().split()[3])
                pwrsub.synchCommand(10,"sequencePower %d" % (i));
                pwrsub.synchCommand(10,"setNamedPowerOn %d heater False" % (i));
            except Exception, e:
                print "%s: failed to turn on current %s!" % (rebname,pwr)
                raise Exception(e)

            time.sleep(2.0)


# Insure the that the RCE is talking to the REBs before starting the checks
            chkreb = True
            print "Rebooting the RCE after a 5s wait"
            time.sleep(5.0)
            sout = subprocess.check_output("$HOME/rebootrce.sh", shell=True)
            print sout
            time.sleep(3.0)
    
# perform checks
            try:
                if 'digital' in pwron :
                    check_currents(i,"digital","DigI",6.,800.,chkreb)
                if 'analog' in pwron :
                    check_currents(i,"analog","AnaI",6.,610.,chkreb)
                if 'od' in pwron :
                    time.sleep(5.0)
                    check_currents(i,"OD","ODI",6.,190.,chkreb)
                if 'clockhi' in pwron :
                    check_currents(i,"clockhi","ClkHI",6.0,300.,chkreb)
                if 'clocklo' in pwron :
                    time.sleep(5.0)
                    check_currents(i,"clocklo","ClkLI",6.,300.,chkreb)
            except Exception, e:
                print "%s: CURRENT CHECK FAILED! %s" % (rebname,e)
                status_value = False
                raise Exception
                break
            time.sleep(2)

    print "setting tick and monitoring period to 10s"
    ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
    ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");
    

    if status_value :
        print "DONE with successful powering of REB PS lines for "
        print rebids
    else :
        print "FAILED to turn on all requested rebs"

print "stop tstamp: %f" % time.time()
