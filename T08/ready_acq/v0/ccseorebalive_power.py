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

    print "verifying that the current is within limits"
    if (chkreb) :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f mAmps, REB value is %8.3f mAmps" % (rebname,pwr_chan,cur_ps,cur_reb)
    else :
        stat = "%s: - checking %10.10s : OK - PS value is %8.3f mAmps, REB not yet ON" % (rebname,pwr_chan,cur_ps)

        print " ... stat = ",stat
    if (cur_ps < low_lim or cur_ps> high_lim) :
        pwrsub.synchCommand(10,"sequencePower %d False" % (rebid)).getResult();
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
    ts8sub  = CCS.attachSubsystem("%s" % ts8);
    pwrsub  = CCS.attachSubsystem("rebps");
    pwrmainsub  = CCS.attachSubsystem("rebps/MainCtrl");


    status_value = True

    result = pwrsub.synchCommand(10,"getChannelNames");
    channames = result.getResult()

#    print channames

    rebnames = ts8sub.synchCommand(10,"getREBDeviceNames").getResult()


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
        for rebid in rebnames :
            rebnum = rebid[len(rebid)-1]
            print "rebid = %s" % rebnum
            idmap.append("%d:%d" % (int(rebnum),int(rebnum)))

    print "Will attempt to power on:"
    for ids in idmap :
        pwrid = int(ids.split(":")[0])
        rebid = int(ids.split(":")[1])
        print "power line %d for REB ID %d" % (pwrid,rebid)


    print "setting tick and monitoring period to 0.5s"

    ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 500");
    ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 500");


#    for rebid in rebnames :
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
#                pwrsub.synchCommand(10,"sequencePower %d False" % (i)).getResult();

            except Exception, e:

                print "%s: FAILED TO TURN POWER OFF! \r\r %s" % (rebname,e)
                raise e

            time.sleep(1.0)

            pwron = ""
            chkreb = False
            

            try:
                print "%s: turning on REB power at %s" % (rebname,time.ctime().split()[3])
                pwrsub.synchCommand(10,"sequencePower %d true" % (i));
            except Exception, e:
                print "%s: failed to turn on REB power!" % (rebname)
                raise Exception(e)


#            time.sleep(2.0)
            print "Rebooting the RCE after a 10s wait"
#            time.sleep(10.0)
#            sout = subprocess.check_output("$HOME/rebootrce.sh", shell=True)
#            print sout
            time.sleep(3.0)
    
            try:
#                print "checking currents"
                
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
#                if 'digital' in pwron :
#                    check_currents(i,"digital","DigI",500.,770.,chkreb)
#                if 'analog' in pwron :
#                    check_currents(i,"analog","AnaI",400.,600.,chkreb)
#                if 'od' in pwron :
#                    check_currents(i,"OD","ODI",60.,120.,chkreb)
#                if 'clockhi' in pwron :
#                    check_currents(i,"clockhi","ClkI",100.0,300.,chkreb)
#                if 'clocklo' in pwron :
#                    check_currents(i,"clocklo","ClkI",100.,300.,chkreb)
##               check_currents(i,"heater","???",0.100,0.300,chkreb)
            except Exception, e:
                print "%s: CURRENT CHECK FAILED! %s" % (rebname,e)
                status_value = False
                raise Exception
                break
            time.sleep(2)
                
            if status_value :
                print "PROCEED TO TURN ON REB CLOCK AND RAIL VOLTAGES"
                print "CCSCCDTYPE=",CCSCCDTYPE
                print "dropping all changes to insure that the base configuration is in use"
                ts8sub.synchCommand(10,"dropAllChanges")
                ts8sub.synchCommand(10,"showREBCfg %d" % rebid)

                if 'e2v' in CCSCCDTYPE.lower() :
                    if not 'e2v' in ts8sub.synchCommand(10,"getCcdType").getResult():
                        for iwrn in range(2):
                            print "Inconsistent sensor and RTM type ABORTING!!!"
                        raise Exception("Inconsistent sensor and RTM type ABORTING!!!")

                    for iwrn in range(2):
                        print "USING CONFIGURATION CATEGORY ***** E2V *****   ABORT IF THIS IS NOT OK!"
#                    ts8sub.synchCommand(10,"loadCategories Rafts:e2v")
#                    ts8sub.synchCommand(10,"loadCategories RaftsLimits:e2v")
                elif 'itl' in CCSCCDTYPE.lower() :
                    if not 'itl' in ts8sub.synchCommand(10,"getCcdType").getResult():
                        for iwrn in range(2):
                            print "Inconsistent sensor and RTM type ABORTING!!!"
                        raise Exception("Inconsistent sensor and RTM type ABORTING!!!")
                    for iwrn in range(2):
                        print "USING CONFIGURATION CATEGORY ***** ITL *****   ABORT IF THIS IS NOT OK!"
#                    ts8sub.synchCommand(10,"loadCategories Rafts:itl")
#                    ts8sub.synchCommand(10,"loadCategories RaftsLimits:itl")
                else :
                    for iwrn in range(2):
                        print "UNABLE TO DETERMINE REQUIRED CONFIG CATEGORY ... ABORT!!!"
                    raise Exception("UNABLE TO DETERMINING REQUIRED CONFIG CATEGORY!")

                print "Waiting for 3 seconds to give time to abort (kill interpreter) if necessary"

                time.sleep(3.0)
                try:
#                    stat = ts8sub.synchCommand(1000,"powerOn %d" % rebid).getResult()
                    print "calling powerCCDsOn now ..."
                    stat = ts8sub.synchCommand(300,"R00.Reb%d powerCCDsOn" % rebid).getResult()
                    print "powerCCDsOn execution completed. Now loading ASPICS"
                    stat = ts8sub.synchCommand(300,"R00.Reb%d loadAspics true" % rebid).getResult()
                    print "Now pausing 5s."
                    time.sleep(5.0)
                    try:
                        print stat.replace("\n","\r\n")
                    except:
                        pass
                    print "---------------List of low current channels ------------------"
                    try:
                        for ln in stat.split("\n"):
                            if "BELOW LOW" in ln.upper() :
                                print ln
                    except:
                        pass
                    print "---------------End of list of low current channels ------------"
                    print "---------------CCD Temperatures as retrieved from getChannelValue are -----"
                    for ccdnum in range(3) :
                        reb_chan = "CCDTemp%d" % ccdnum
                        ccdtemp = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.%s" % (rebid,reb_chan)).getResult()

                        f_ccdtemp = -999.
                        try:
                            f_ccdtemp = float(ccdtemp)
                        except:
                            pass
 
                        print "%s : %s = %8.3f " % (rebname,reb_chan,f_ccdtemp)

                
                    print "------ %s Complete ------\n" % rebname
                except RuntimeException, e:
                    print "There was an Exception. Sleeping 5s to give operator chance to read output."
                    time.sleep(5.0)
                    print "\n\n\n The exception \n\n\n"
                    print e
                    print "\n\n\n"
                    print "setting tick and monitoring period to 10s"

                    ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
                    ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");
                    raise e
                except Exception, e:
                    print e
                    print "setting tick and monitoring period to 10s"

                    ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
                    ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");

                    raise e

    print "setting tick and monitoring period to 10s"

    ts8sub.synchCommand(10,"monitor-update change taskPeriodMillis 10000");
    ts8sub.synchCommand(10,"monitor-publish change taskPeriodMillis 10000");

    if status_value :
        print "SUCCESSFUL"
#        print rebnames
    else :
        print "FAILED!"

print "stop tstamp: %f" % time.time()
