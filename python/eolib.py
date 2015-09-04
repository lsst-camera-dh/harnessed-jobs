#! /usr/bin/env python 
# eolib.py
#
# functions that are used by the CCS teststand acquisition jobs

import time
from org.lsst.ccs.scripting import *
    

###############################################################################
# create a time stamp
def tstamp():
    tstamp=time.strftime("%Y%m%d%H%M%S")
    return tstamp
    
###############################################################################
# read in the site.cfg file and get keyword value
# Find the first occurance and return string. Return default value if not found.
def getCfgVal(cfgfile, name, default="NOT FOUND"):
    value = default
    fp = open(cfgfile,"r");
    for line in fp:
        tokens = str.split(line)
        if (len(tokens) >= 2): 
            if (tokens[0].upper() == name.upper() ):
                value = tokens[1]
                break
    fp.close();
    return value

###############################################################################
# Read the flux vs wl calibration file and get flux associated with a wl
# Find the first occurance of the reuested wl and return value
def getFluxcalVal(calfile, wl):
    wl = float(wl)
    fp = open(calfile,"r");
    for line in fp:
        tokens = str.split(line)
        if (len(tokens) > 0): 
            if ((tokens[0] == 'fluxcal') and (float(tokens[1]) == wl)):
                break
    fp.close();
    return float(tokens[2])

###############################################################################
# Read the flux vs wl calibration file and get flux associated with a wl
# Find the first occurance of the reuested wl or the next higher and return 
# a value, either of the wavelength requested (if found) or interpolated.
def getFluxcalFlux(calfile, wl):
    wl = float(wl)
    wavelengths = []
    fluxes = []
    fp = open(calfile,"r");
    for line in fp:
        tokens = str.split(line)
        if (len(tokens) > 0): 
            if (tokens[0] == 'fluxcal'): 
                wavelengths.append(float(tokens[1]))
                fluxes.append(float(tokens[2]))
    fp.close();
    waves = sorted(wavelengths)
    for i in range(len(wavelengths)):
        if (wavelengths[i] > wl):
	    break
    low = wavelengths[i-1]
    high = wavelengths[i]
    if (low == wl):  # we found an exact match
        return getFluxcalVal(calfile, wl)
    else:
        lowf = getFluxcalVal(calfile, low) 
        highf = getFluxcalVal(calfile, high) 
	flux = lowf - (((wl-low)/(high-low)) * (lowf - highf))
    return flux

###############################################################################
# expCalc: compute the exposure time required to reach a target signal level 
# at a specified wavelength
def expCalc(calfile, wl, target, nd=0.0):
    flux = getFluxcalFlux(calfile, wl) / pow(10,float(nd))
    exptime = float(target)/float(flux)
    return exptime

###############################################################################
# expCheck: check the exposure time required to reach a target signal level 
# at a specified wavelength is OK and optionally adjust ND filter.
def expCheck(calfile, lab, target, wl, hi_lim, lo_lim, test='TEST', use_nd=False):

#    caldir  = getCfgVal(lab['config'],'BASE_DIR')+'/system/fluxcal'
#    calfiles = sorted(glob.glob(caldir+'/fluxcal*.txt')) 
#    calfile = calfiles[len(calfiles)-1]
    
    ndfilter = float(getCfgVal(calfile, 'ND_FILTER', default='2.0'))

    exptime = expCalc(calfile, wl, target)
    if (exptime < lo_lim):
        if (use_nd == True):
            print "%s : Exposure time %6.2f is below lower limit." % (str.upper(test), exptime)
#            lab['monochromator'].setFilter(5) # put the nd filter in place
            exptime = expCalc(calfile, wl, target, nd=ndfilter)
            print "%s : Exp time with ND %4.2f Filter = %6.2f" % (str.upper(test), ndfilter, exptime)
        else:
            print "%s : Exposure time limited to %6.2f sec." % (str.upper(test), lo_lim)
            exptime = lo_lim
    if (exptime > hi_lim):
        print "%s : Exposure time limited to %6.2f sec." % (str.upper(test), hi_lim)
        exptime = hi_lim
    return exptime

###############################################################################
# EOgetCCSVersions: getCCSVersions
def EOgetCCSVersions(tssub,cdir):
    result = tssub.synchCommand(10,"getCCSVersions");
    ccsversions = result.getResult()
    ccsvfiles = open("%s/ccsversion" % cdir,"w");
    ccsvfiles.write("%s" % ccsversions)
    ccsvfiles.close()
#    print "ccsversions = %s" % ccsversions
    ssys = ""

    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""
    for line in str(ccsversions).split("\t"):
        tokens = line.split()
        if (len(tokens)>2) :
            if ("ts" in tokens[2]) :
                ssys = "ts"
            if ("archon" in tokens[2]) :
                ssys = "archon"
#            print "tokens[1] = %s " % tokens[1]
            if (tokens[1] == "Version:") :
                print "%s - version = %s" % (ssys,tokens[2])
                if (ssys == "ts") :
                    ts_version = tokens[2]
                if (ssys == "archon") :
                    archon_version = tokens[2]
            if (len(tokens)>3) :
                if (tokens[2] == "Rev:") :
                    print "%s - revision = %s" % (ssys,tokens[3])
                    if (ssys == "ts") :
                        ts_revision = tokens[3]
                    if (ssys == "archon") :
                        archon_revision = tokens[3]
#                print "tokens[2] = %s " % tokens[2]
#       print "\nCCSVersions line = %s \n" % line
    return(ts_version,archon_version,ts_revision,archon_revision)
###############################################################################
# EOjobPrep: perform setup need from running standard EO jobs
def EOSetup(tssub,acffile,vac_outlet,arcsub,biassub,pdsub,pdusub,state1="setTSReady",state2="setTSTEST"):

# Initialization
    print "doing initialization"

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

# move TS to ready state
    result = tssub.synchCommand(60,state1);
    reply = result.getResult();
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();

    print "test stand in ready state, now the controller will be configured. time = %f" % time.time()

    print "initializing archon controller with file %s" % acffile
    print "Loading configuration file into the Archon controller"
    result = arcsub.synchCommand(20,"setConfigFromFile",acffile);
    reply = result.getResult();
    print "Applying configuration"
    result = arcsub.synchCommand(25,"applyConfig");
    reply = result.getResult();
    print "Powering on the CCD"
    result = arcsub.synchCommand(30,"powerOnCCD");
    reply = result.getResult();
    time.sleep(30.);

    print "set controller parameters for an exposure with the shutter closed"
    arcsub.synchCommand(10,"setAcqParam","Nexpo");
    arcsub.synchCommand(10,"setParameter","Expo","1");
    arcsub.synchCommand(10,"setFetch_timeout",500000);
# move to TS acquisition state
    print "setting acquisition state"

    result = tssub.synchCommand(60,state2);
    rply = result.getResult();

#check state of ts devices
    print "wait for ts state to become ready";
    tsstate = 0
    starttim = time.time()
    while True:
        print "checking for test stand to be ready for acq";
        result = tssub.synchCommand(10,"isTestStandReady");
        tsstate = result.getResult();
# the following line is just for test situations so that there would be no waiting                                         
        tsstate=1;
        if ((time.time()-starttim)>240):
            print "Something is wrong ... we will never make it to a runnable state"
            exit
        if tsstate!=0 :
            break
        time.sleep(5.)
#put in acquisition state
    print "We are ready to go! Ramping the BP bias voltage now."
    result = tssub.synchCommand(120,"goTestStand");
    rply = result.getResult();
# get the glowing vacuum gauge off
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,False);
    rply = result.getResult();
# it takes time for the glow to fade
    time.sleep(5.)




###############################################################################
#def findCalfile(lab):
#    caldir  = getCfgVal(lab['config'],'BASE_DIR')+'/system/fluxcal'
#    calfiles = sorted(glob.glob(caldir+'/fluxcal*.txt')) 
#    calfile = calfiles[len(calfiles)-1]
#    return calfile
