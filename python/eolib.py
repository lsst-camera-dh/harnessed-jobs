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



    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    for line in str(ccsversions).split("\t"):
        tokens = line.split()
        if ("Project   " in line) :
            ssys = ""
            if ("teststand" in tokens[2]) :
                ssys = "ts"
            if ("archon" in tokens[2]) :
                ssys = "archon"
        if ("Version:" in line) :
            if (ssys == "ts") :
                ts_version = tokens[2]
            if (ssys == "archon") :
                archon_version = tokens[2]
        if ("Rev:" in line) :
            print "%s - revision = %s" % (ssys,tokens[3])
            if (ssys == "ts") :
                ts_revision = tokens[3]
            if (ssys == "archon") :
                archon_revision = tokens[3]
    return(ts_version,archon_version,ts_revision,archon_revision)

###############################################################################
# EOgetTS8CCSVersions: getTS8CCSVersions
def EOgetTS8CCSVersions(tssub,cdir):
    result = tssub.synchCommand(10,"getCCSVersions");
    ccsversions = result.getResult()
    ccsvfiles = open("%s/ccsversion" % cdir,"w");
    ccsvfiles.write("%s" % ccsversions)
    ccsvfiles.close()



    ts_version = ""
    ts8_version = ""
    power_version = ""

    ts_revision = ""
    ts8_revision = ""
    power_revision = ""

    for line in str(ccsversions).split("\t"):
        tokens = line.split()
        if ("Project   " in line) :
            ssys = ""
            if ("teststand" in tokens[2]) :
                ssys = "ts"
            if ("ts8" in tokens[2]) :
                ssys = "ts8"
            if ("power" in tokens[2]) :
                ssys = "power"
        if ("Version:" in line) :
            if (ssys == "ts") :
                ts_version = tokens[2]
            if (ssys == "ts8") :
                ts8_version = tokens[2]
            if (ssys == "power") :
                power_version = tokens[2]
        if ("Rev:" in line) :
            if len(tokens)>3 :
                print "%s - revision = %s" % (ssys,tokens[3])
                if (ssys == "ts") :
                    ts_revision = tokens[3]
                if (ssys == "ts8") :
                    ts8_revision = tokens[3]
                if (ssys == "power") :
                    power_revision = tokens[3]
    return(ts_version,ts8_version,power_version,ts_revision,ts8_revision,power_revision)

###############################################################################
# EOTS8SetupCCDInfo: setup CCD specific info for running standard EO TS8 jobs
def EOTS8SetupCCDInfo(ts8sub,rebpssub,ccdnames,ccdmanunames):



    geo = ts8sub.synchCommand(2,"printGeometry 3").getResult();
    for line in geo.split('\n') :
        if len(line.split('.'))==3  :
            linelen = len(line)
            slot = line[linelen-2] + line[linelen-1];
            sn = ccdnames[slot]
            ccdid = line.split(' ')[1]
            ts8sub.synchCommand(2,"setLsstSerialNumber %s %s" % (ccdid,sn))
            manu_sn = ccdmanunames[slot]
            rebid = int(line[linelen-2])
            ccdnum = int(line[linelen-1])
            if (len(manu_sn)>0) :
                ts8sub.synchCommand(10,"setManufacturerSerialNumber %s %s" % (ccdid,manu_sn))
            ccdtemp  = ts8sub.synchCommand(10,"getChannelValue R00.Reb%d.CCDTemp%d"%(rebid,ccdnum)).getResult()
            print ccdid,": CCDTemp = ",ccdtemp

            ts8sub.synchCommand(10,"setMeasuredCCDTemperature %s %f"%(ccdid,float(ccdtemp)))
            hv = rebpssub.synchCommand(10,"getChannelValue REB%d.hvbias.VbefSwch"%(rebid)).getResult()
            print ccdid,": HVbias = ",hv

            ts8sub.synchCommand(10,"setMeasuredCCDBSS %s %f"%(ccdid,float(hv)))

###############################################################################
# EOTS8Setup: perform setup needed for running standard EO TS8 jobs
def EOTS8Setup(tssub,ts8sub,rebpssub,raftid,ccdtype,cdir,seqfile,vac_outlet,state1="setTSReady",state2="setTSTEST"):

# Pre TS Initialization
#    tssub.synchCommand(11000,"eoSetupPreCfg",state1).getResult();


# full path causes length problem: /home/ts8prod/lsst/redhat6-x86_64-64bit-gcc44/test/jh_inst/0.3.23/harnessed-jobs-0.3.23/config/BNL/sequencer-ts8-ITL-v4.seq                                                             
    print "sequencer file = %s " % seqfile
    result = ts8sub.synchCommand(90,"loadSequencer",seqfile);



# not activated until ts subsystem timeout adjusted
#   if (False) :
#       try:
#           press = vqmsub.synchCommand(30,"readPressure").getResult();
#           if (press>0.0) :
#               try:
#                   reply = tssub.synchCommand(30,"disconnectVQM").getResult();
#               except:
#                   pass
#               reply = pdusub.synchCommand(360,"ts/PDU setOutlet %d false" % vac_outlet).getResult();
#       except:
#           pass


# Post TS Initialization
#    tssub.synchCommand(11000,"eoSetupPostCfg",vac_outlet,state2).getResult();

###############################################################################
# EOSetup: perform setup needed for running standard EO jobs
def EOSetup(tssub,ccdid,ccdtype,cdir,acffile,vac_outlet,arcsub,state1="setTSReady",state2="setTSTEST"):

    result = arcsub.synchCommand(10,"setHeader","MonochromatorWavelength",-1.0)
    result = arcsub.synchCommand(10,"setCCDnum",ccdid)
    result = arcsub.synchCommand(10,"setLSSTnum",ccdid)

# Pre Archon TS Initialization
    result = tssub.synchCommand(11000,"eoSetupPreCfg",state1);
    reply = result.getResult();
# Archon Initialization
    result = arcsub.synchCommand(500,"eoSetup",acffile,ccdtype);
    reply = result.getResult();
# Post Archon TS Initialization
    try:
        reply = tssub.synchCommand(100,"disconnectVQM").getResult();
    except:
        pass
    result = tssub.synchCommand(200,"eoSetupPostCfg",vac_outlet,state2);
    reply = result.getResult();

    result = arcsub.synchCommand(10,"getKpixRate");
    kpixrate = result.getResult();

    result = arcsub.synchCommand(10,"setHeader","PixelReadRate",kpixrate/1000.)

#    result = arcsub.synchCommand(10,"setDefaultCCDType ITL_OVERSCAN_64")
    result = arcsub.synchCommand(10,"setCCDOverScans",50)


###############################################################################
#def findCalfile(lab):
#    caldir  = getCfgVal(lab['config'],'BASE_DIR')+'/system/fluxcal'
#    calfiles = sorted(glob.glob(caldir+'/fluxcal*.txt')) 
#    calfile = calfiles[len(calfiles)-1]
#    return calfile
