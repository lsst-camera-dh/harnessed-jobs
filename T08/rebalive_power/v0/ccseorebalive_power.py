###############################################################################
# REB-PS safe power on
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
import subprocess
#import siteUtils


CCS.setThrowExceptions(True);

#################################################################
#   Check that PS current levels are within acceptable range
#################################################################
def check_currents(rebid,pwr_chan,reb_chan,low_lim,high_lim,chkreb):

    print "Retrieving REB PS current %s " % pwr_chan
    cur_ps = pwrsub.synchCommand(10,"getChannelValue REB%d.%s.IaftLDO" % (rebid,pwr_chan)).getResult()
    print "Retrieving REB current %s " % reb_chan
    cur_reb = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()

    print "verifying that the current is with limits"
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
#            pwrsub.synchCommand(10,"setNamedPowerOn %d %s False" % (rebid,pwr))
#            stat = "%s: Current %s with value %f differs by > 20%% to current from reb channel %s with value %f. POWER TO THIS CHANNEL HAS BEEN SHUT OFF!" % (rebname,pwr_chan,cur_ps,reb_chan,cur_reb)
#            raise Exception(stat)

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
 #   sys.stdout = open("%s/rebalive_results.txt" % cdir, "w")
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
    pwrsub  = CCS.attachSubsystem("ccs-rebps");
    pwrmainsub  = CCS.attachSubsystem("ccs-rebps/MainCtrl");


    status_value = True

    result = pwrsub.synchCommand(10,"getChannelNames");
    channames = result.getResult()

#    print channames
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
    ts8sub.synchCommand(10,"change tickMillis 100");
#    ts8sub.synchCommand(10,"setTickMillis 100")

#    for rebid in rebids :
    for ids in idmap :
        pwrid = int(ids.split(":")[0])
        rebid = int(ids.split(":")[1])

        if status_value :
            i = pwrid
            rebname = 'REB%d' % i
            print "****************************************************"
            print " Starting power ON procedure for REB power line %s and REB %s" % (pwrid,rebname)
            print "****************************************************"


# verify that all power is OFF
            try:
                stat = ts8sub.synchCommand(300,"R00.Reb%d setBackBias false" % rebid).getResult()
                stat = ts8sub.synchCommand(300,"powerOff %d" % rebid).getResult()

#                result = pwrsub.synchCommand(10,"setNamedPowerOn",i,"master",False);
                result = pwrsub.synchCommand(20,"setNamedPowerOn %d master False" % i);
            except Exception, e:

                print "%s: FAILED TO TURN POWER OFF! \r\r %s" % (rebname,e)
                raise e

            time.sleep(3.0)

            pwron = ""
# attempt to apply the REB power -- line by line
            powers = ['master', 'digital', 'analog', 'clockhi', 'clocklo', 'heater', 'od']
            chkreb = False

            for pwr in powers :
                pwron = pwron + pwr + " "
                if 'clockhi' in pwr:
                    chkreb = True
                    print "Rebooting the RCE after a 5s wait"
                    time.sleep(5.0)
                    sout = subprocess.check_output("$HOME/rebootrce.sh", shell=True)
                    print sout
                    time.sleep(3.0)
                try:
                    print "%s: turning on %s power at %s" % (rebname,pwr,time.ctime().split()[3])
                    pwrsub.synchCommand(10,"setNamedPowerOn %d %s True" % (i,pwr));
                except Exception, e:
                    print "%s: failed to turn on current %s!" % (rebname,pwr)
                    raise Exception(e)

                time.sleep(2.0)
    
                try:
#                    print "checking currents"
                    
                    if 'digital' in pwron :
                        check_currents(i,"digital","DigI",6.,800.,chkreb)
                    if 'analog' in pwron :
                        check_currents(i,"analog","AnaI",6.,610.,chkreb)
                    if 'od' in pwron :
                        check_currents(i,"OD","ODI",6.,190.,chkreb)
                    if 'clockhi' in pwron :
                        check_currents(i,"clockhi","ClkI",6.0,300.,chkreb)
                    if 'clocklo' in pwron :
                        check_currents(i,"clocklo","ClkI",6.,300.,chkreb)
#                    if 'digital' in pwron :
#                        check_currents(i,"digital","DigI",500.,770.,chkreb)
#                    if 'analog' in pwron :
#                        check_currents(i,"analog","AnaI",400.,600.,chkreb)
#                    if 'od' in pwron :
#                        check_currents(i,"OD","ODI",60.,120.,chkreb)
#                    if 'clockhi' in pwron :
#                        check_currents(i,"clockhi","ClkI",100.0,300.,chkreb)
#                    if 'clocklo' in pwron :
#                        check_currents(i,"clocklo","ClkI",100.,300.,chkreb)
##                   check_currents(i,"heater","???",0.100,0.300,chkreb)
                except Exception, e:
                    print "%s: CURRENT CHECK FAILED! %s" % (rebname,e)
                    status_value = False
                    raise Exception
                    break
                time.sleep(2)
            if status_value :
                print "PROCEED TO TURN ON REB CLOCK AND RAIL VOLTAGES"
#    load default configuration
                ts8sub.synchCommand(10,"loadCategories Rafts:itl")
                ts8sub.synchCommand(10,"loadCategories RaftsLimits:itl")
                try:
                    stat = ts8sub.synchCommand(300,"powerOn %d" % rebid).getResult()
                    print stat.replace("\n","\r\n")
                    print "---------------List of low current channels ------------------"
                    for ln in stat:
                        if "LOW CURRENT" in ln.upper() :
                            print ln
                    print "---------------End of list of low current channels ------------"
                    print "---------------CCD Temperatures as retrieved from getChannelValue are -----"
                    for ccdnum in range(3) :
                        reb_chan = "CCDTemp%d" % ccdnum
                        ccdtemp = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()
                        print "%s : %s = %8.3f " % (rebname,reb_chan,ccdtemp)

                
                    print "------ %s Complete ------\n" % rebname
                except RuntimeException, e:
                    print e
                    print "setting tick and monitoring period to 10s"
                    ts8sub.synchCommand(10,"change tickMillis 10000");
                    raise e
                except Exception, e:
                    print e
                    print "setting tick and monitoring period to 10s"
                    ts8sub.synchCommand(10,"change tickMillis 10000");
                    raise e

    print "setting tick and monitoring period to 10s"
    ts8sub.synchCommand(10,"change tickMillis 10000");

    if status_value :
        print "DONE with successful powering of"
        print rebids
    else :
        print "FAILED to turn on all requested rebs"

print "stop tstamp: %f" % time.time()
