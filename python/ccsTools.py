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
        self['ts'] = 'ts'
        self['archon'] = 'archon'
        self['tsCWD'] = _quote(os.getcwd())
        self['labname'] = _quote(siteUtils.getSiteName())
        self['CCDID'] = _quote(siteUtils.getUnitId())
        self._read(os.path.join(siteUtils.getJobDir(), configFile))
    def _read(self, configFile):
        if configFile is None:
            return
        configDir = siteUtils.configDir()
        for line in open(configFile):
            key, value = line.strip().split("=")
            self[key.strip()] = _quote(os.path.join(configDir, value.strip()))
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

def ccsProducer(jobName, ccsScript, makeBiasDir=True, verbose=True):
    """
    Run the CCS data acquistion script under the CCS jython interpreter.
    """
    if makeBiasDir:
        os.mkdir("bias")

    ccs = CcsJythonInterpreter("ts")
    ccs.syncExecution("ts = 'ts2'");
    ccs.syncExecution("archon = 'archon'");
    setup = CcsSetup('%s.cfg' % jobName)
    result = ccs.syncScriptExecution(siteUtils.jobDirPath(ccsScript), setup(),
                                     verbose=verbose)
    output = open("%s.log" % jobName, "w")
    output.write(result.getOutput())
    output.close()

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

def ccsValidator(jobName, acqfilelist='acqfilelist', statusFlags=('stat',)):
    try:
        hdrtools.updateFitsHeaders(acqfilelist)
    except IOError:
        pass

#    ccsTrendingPlots(('ts/ccdtemperature', 'ts/dewarpressure'), jobName,
#                     os.path.join(siteUtils.configDir(), 'ccs_trending.cfg'))

    results = []

    statusFile = open("status.out")
    statusAssignments = {}
    for flag in statusFlags:
        value = int(statusFile.readline().strip())
        statusAssignments[flag] = value
    
    results.append(lcatr.schema.valid(lcatr.schema.get(jobName), 
                                      **statusAssignments))

    # @todo Fix this. Copying these files should not be necessary.
#    jobdir = siteUtils.getJobDir()
#    os.system("cp -vp %s/*.fits ." % jobdir)   

    # @todo Sort out which files really need to be curated.
    files = glob.glob('*.fits')
    files = files+glob.glob('*log*')
    files = files+glob.glob('*summary*')
    files = files+glob.glob('*.png')
    print "The files that will be registered in lims from %s are:" % os.getcwd()
    for line in files :
        print "%s" % line
    data_products = [lcatr.schema.fileref.make(item) for item in files]
    results.extend(data_products)
    results.append(siteUtils.packageVersions())

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()
