import os
import glob
import subprocess
from collections import OrderedDict
if os.environ.has_key('SIMDIR'):
    from PythonBindingSimulator import CcsJythonInterpreter
else:
    from PythonBinding import CcsJythonInterpreter
import siteUtils
import hdrtools
import lcatr.schema

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
        self['tsCWD'] = os.getcwd()
        self['labname'] = siteUtils.getSiteName()
        self['CCDID'] = siteUtils.getUnitId()
        self._read(os.path.join(siteUtils.getJobDir(), configFile))
    def _read(self, configFile):
        if configFile is None:
            return
        configDir = siteUtils.configDir()
        for line in open(configFile):
            key, value = line.strip().split("=")
            self[key.strip()] = os.path.join(configDir, value.strip())
    def __call__(self):
        """
        Return the setup commands for the CCS script.
        """
        # Set the local variables.
        commands = ['%s = %s' % item for item in self.items()]
        # Append path to the modules used by the jython code.
        commands.append('import sys')
        commands.append('sys.path.append(%s)' % siteUtils.pythonDir())
        return '\n'.join(commands)

def ccsProducer(jobName, ccsScript, makeBiasDir=True, verbose=True):
    """
    Run the CCS data acquistion script under the CCS jython interpreter.
    """
    if makeBiasDir:
        os.mkdir("bias")

    ccs = CcsJythonInterpreter()
    setup = CcsSetup('%s.cfg' % jobName)
    result = ccs.syncScriptExecution(siteUtils.jobDirPath(ccsScript), setup(),
                                     verbose=verbose)
    output = open("%s.log" % jobName, "w")
    output.write(result.getOutput())
    output.close()
    
def ccsValidator(jobName, acqfilelist='acqfilelist', statusFlags=('stat',)):
    try:
        hdrtools.updateFitsHeaders(acqfilelist)
    except IOError:
        pass

    # @todo Implement trending plot generation using python instead of
    # gnuplot
    sitedir = os.path.join(os.environ['VIRTUAL_ENV'], "TS3_JH_acq", "site")
    plotter = os.path.join(sitedir, "dotemppressplots.sh")
    if os.path.isfile(plotter):
        subprocess.call(plotter, shell=True)

    results = []

    statusFile = open("status.out")
    statusAssignments = {}
    for flag in statusFlags:
        value = int(statusFile.readline().strip())
        statusAssignments[flag] = value
    
    results.append(lcatr.schema.valid(lcatr.schema.get(jobName), 
                                      **statusAssignments))

    # @todo Fix this. Copying these files should not be necessary.
    jobdir = siteUtils.getJobDir()
    os.system("cp -vp %s/*.fits ." % jobdir)   

    # @todo Sort out which files really need to be curated.
    files = glob.glob('*.fits,*values*,*log*,*summary*,*.dat,*.png,bias/*.fits')
    data_products = [lcatr.schema.fileref.make(item) for item in files]
    results.extend(data_products)

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()
