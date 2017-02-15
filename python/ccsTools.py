

import os
import glob
import subprocess
from collections import OrderedDict
import datetime
import numpy as np
import pylab
import matplotlib
if os.environ.has_key('SIMDIR'):
    from PythonBindingSimulator import CcsJythonInterpreter
else:
    from PythonBinding import CcsJythonInterpreter
import siteUtils
import hdrtools
from DbInterface import DbInterface
import lcatr.schema

_quote = lambda x : "'%s'" % x

class CcsSetup(OrderedDict):
    """
    The context-specific setup commands for executing a CCS script
    written in jython.  These commands set variables and paths that
    are known in the calling python code and which are needed by the
    jython script.
    """
    def __init__(self, configFile):
        """
        configFile contains the names of the site-specific
        configuration files.  File basenames are provided in
        configFile, and the full paths are constructed in the
        _read(...) method.
        """
        super(CcsSetup, self).__init__()
        if os.environ.has_key('CCS_TS'):
            self['ts']=_quote(os.getenv('CCS_TS'))
        else:
            self['ts'] = _quote('ts')
        if os.environ.has_key('CCS_ARCHON'):
            self['archon']=_quote(os.getenv('CCS_ARCHON'))
        else:
            self['archon'] = _quote('archon')
        if os.environ.has_key('CCS_VAC_OUTLET'):
            self['vac_outlet']=os.getenv('CCS_VAC_OUTLET')
# there is no default for vac_outlet - if there is a script that needs
# it and it has not been defined then I want it to crash
        if os.environ.has_key('CCS_CRYO_OUTLET'):
            self['cryo_outlet']=os.getenv('CCS_CRYO_OUTLET')
# there is no default for cryo_outlet - if there is a script that needs
# it and it has not been defined then I want it to crash
        if os.environ.has_key('CCS_PUMP_OUTLET'):
            self['pump_outlet']=os.getenv('CCS_PUMP_OUTLET')
# there is no default for pump_outlet - if there is a script that needs
# it and it has not been defined then I want it to crash
        self['tsCWD'] = _quote(os.getcwd())
        self['labname'] = _quote(siteUtils.getSiteName())
        self['jobname'] = _quote(siteUtils.getJobName())
        self['CCDID'] = _quote(siteUtils.getUnitId())
        self['UNITID'] = _quote(siteUtils.getUnitId())
        self['LSSTID'] = _quote(siteUtils.getLSSTId())
        ccdnames = {}
        ccdmanunames = {}
        ccdnames,ccdmanunames = siteUtils.getCCDNames()
        print "retrieved the following LSST CCD names list"
        print ccdnames
        print "retrieved the following Manufacturers CCD names list"
        print ccdmanunames
        for slot in ccdnames :
            print "CCD %s is in slot %s" % (ccdnames[slot],slot)
            self['CCD%s'%slot] = _quote(ccdnames[slot])
        for slot in ccdmanunames :
            print "CCD %s is in slot %s" % (ccdmanunames[slot],slot)
            self['CCDMANU%s'%slot] = _quote(ccdmanunames[slot])
        try:
            self['RUNNUM'] = _quote(siteUtils.getRunNumber())
        except:
            self['RUNNUM'] = "no_lcatr_run_number"
        self._read(os.path.join(siteUtils.getJobDir(), configFile))
        CCDTYPE = _quote(siteUtils.getUnitType())
        print "CCDTYPE = %s" % CCDTYPE
        self['sequence_file'] = _quote("NA")
        self['acffile'] = self['itl_acffile']
        self['CCSCCDTYPE'] = _quote("ITL")
        if ("RTM" in CCDTYPE.upper() or "ETU" in CCDTYPE.upper() ) :
            if ("e2v" in CCDTYPE) :
                self['CCSCCDTYPE'] = _quote("E2V")
                self['acffile'] = self['e2v_acffile']
                self['sequence_file'] = self['e2v_seqfile']
            else :
                self['CCSCCDTYPE'] = _quote("ITL")
                self['acffile'] = self['itl_acffile']
                self['sequence_file'] = self['itl_seqfile']
            os.system("cp -vp %s %s" % (self['sequence_file'],self['tsCWD']))
            # now use the local copy
            bb = self['sequence_file'],split("/")
            self['sequence_file'] = "%s/%s" % (self['tsCWD'],bb[len(bb)-1])
            print "The sequence file to be used is %s" % self['sequence_file']
        else :
            if ("ITL" in CCDTYPE) :
                self['CCSCCDTYPE'] = _quote("ITL")
                self['acffile'] = self['itl_acffile']
            if ("e2v" in CCDTYPE) :
                self['CCSCCDTYPE'] = _quote("E2V")
                self['acffile'] = self['e2v_acffile']
            print "The acffile to be used is %s" % self['acffile']

    def _read(self, configFile):
        if configFile is None:
            return
        configDir = siteUtils.configDir()
        for line in open(configFile):
            key, value = line.strip().split("=")
            self[key.strip()] = _quote(os.path.realpath(os.path.join(configDir, value.strip())))
    def __call__(self):
        """
        Return the setup commands for the CCS script.
        """
        # Set the local variables.
        commands = ['%s = %s' % item for item in self.items()]
        # Append path to the modules used by the jython code.
        commands.append('import sys')
        commands.append('sys.path.append("%s")' % siteUtils.pythonDir())
        return commands

def ccsProducer(jobName, ccsScript, makeBiasDir=False, verbose=True):
    """
    Run the CCS data acquistion script under the CCS jython interpreter.
    """
    if makeBiasDir:
        os.mkdir("bias")

    ccs = CcsJythonInterpreter("ts")
#    setup = CcsSetup('%s.cfg' % jobName)
# change to using a single config from the main config directory
    configDir = siteUtils.configDir()
    setup = CcsSetup('%s/acq.cfg' % configDir )

    result = ccs.syncScriptExecution(siteUtils.jobDirPath(ccsScript), setup(),
                                     verbose=verbose)
    output = open("%s.log" % jobName, "w")
    output.write(result.getOutput())
    output.close()

#    print "purge fluxcal fits files"
#    os.system("rm -v fluxcal*.fits")

def convert_unix_time(millisecs):
    """
    Convert Unix time (in msec) to matplotlib date format.
    """
    secs = np.array(millisecs)/1000.
    fds = matplotlib.dates.date2num([datetime.datetime.fromtimestamp(x)
                                     for x in secs])
    hfmt = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M')
    return fds, hfmt

def ccsTrendingPlots(quantities, outfile_suffix, credentials_file,
                     section='mysql', npts=540, marker='ko',
                     markersize=3):
    """
    Create CCS trending plots.  Currently, the last npts(=540) entries
    in the trending db are plotted.  It's probably better to make a
    explicitly time-based query instead.
    """
    db = DbInterface(credentials_file, section)
    query = lambda x, npts=npts : "select rawdata.tstampmills, rawdata.doubleData from rawdata join datadesc on rawdata.descr_id=datadesc.id where datadesc.name='%s' limit %i" % (x, npts)
    unpack = lambda cursor : zip(*[x for x in cursor])
    for quantity in quantities:
        data = db.apply(query(quantity), cursorFunc=unpack)
        times, hfmt = convert_unix_time(data[0])
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.plot(times, data[1], marker, markersize=markersize)
        ax.xaxis.set_major_formatter(hfmt)
        pylab.xticks(fontsize=8)
        fig.autofmt_xdate()
        pylab.xlabel('Time')
        pylab.ylabel(quantity)
        pylab.savefig('%s_%s.png'%(quantity.replace('/', '_'), outfile_suffix))

def ccsValidator(jobName, acqfilelist='acqfilelist', statusFlags=('stat','teststand_version','teststand_revision','archon_version','archon_revision','ts8_version','ts8_revision','power_version','power_revision')):
    try:
        hdrtools.updateFitsHeaders(acqfilelist)
    except IOError:
        pass

#    ccsTrendingPlots(('ts/ccdtemperature', 'ts/dewarpressure'), jobName,
#                     os.path.join(siteUtils.configDir(), 'ccs_trending.cfg'))

    results = []

    statusAssignments = {}
    try:
        statusFile = open("status.out")
        for flag in statusFlags:
            if (flag=='stat') :
                value = int(statusFile.readline().strip())
                statusAssignments[flag] = value
            else :
                strval = statusFile.readline().strip()
                statusAssignments[flag] = strval
    except IOError:
        for flag in statusFlags:
            statusAssignments[flag] = -1
    

    print "jobName = %s" % jobName
    print "schema = %s" % str(lcatr.schema.get(jobName))

    results.append(lcatr.schema.valid(lcatr.schema.get(jobName), 
                                      **statusAssignments))

    results.append(siteUtils.packageVersions())

    # @todo Fix this. Copying these files should not be necessary.
#    jobdir = siteUtils.getJobDir()
#    os.system("cp -vp %s/*.fits ." % jobdir)   

    # @todo Sort out which files really need to be curated.
    files = glob.glob('*.fits')
    files = files+glob.glob('*/*.fits')
    files = files+glob.glob('*/*.fits.gz')
    files = files+glob.glob('*log*')
#    files = files+glob.glob('*summary*')
    files = files+glob.glob('*.png')
    files = files+glob.glob('*.dat')
    files = files+glob.glob('*.seq')
    files = files+glob.glob('*.xml')
    files = files+glob.glob('*.csv')
    files = files+glob.glob('*.pickles')

    print "The files that will be registered in lims from %s are:" % os.getcwd()
    for line in files :
        print "%s" % line
    data_products = [lcatr.schema.fileref.make(item) for item in files]
    results.extend(data_products)

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()
# now lets crash if that status file wasn't present
# we do this so that the traveler will know that something bad happened
    statusFileCheck = open("status.out")
