"""
PythonBinding simulator for executing ccsTools.ccsProducer(...).
Sensor data for each test are copied from a directory containing a
simulated (or real) dataset for each CCS data acquistion script, which
have names "ccseo<dataset_name>.py"
"""
import os
import subprocess

class AcqSim(object):
    def __init__(self, rootdir):
        self.rootdir = rootdir
        datasets = 'fe55 dark flat qe sflat ppump xtalk fluxcal'.split()
        for dataset in datasets:
            source_path = os.path.join(self.rootdir, dataset, '*')
            exec('self.%(dataset)s_acq = lambda : subprocess.call("cp %(source_path)s .", shell=True)' % locals())

class CcsResult(object):
    def __init__(self, scriptname):
        self.scriptname = scriptname
    def getOutput(self):
        return "Output from %s" % self.scriptname

class CcsJythonInterpreter(object):
    def __init__(self, name=None, host=None, port=4444):
        self.acq = AcqSim(os.environ['SIMDIR'])
    def syncScriptExecution(self, filename, setup_commands=(), verbose=False):
        dataset = filename[len('ccseo'):-3]
        exec('self.acq.%(dataset)s_acq()' % locals())
        return CcsResult(filename)

if __name__ is '__main__':
    os.environ['SIMDIR'] = '../data'
    ccs = CcsJythonInterpreter()

    result = ccs.syncScriptExecution('ccseofe55.py')
    print result.getOutput()

    result = ccs.syncScriptExecution('ccseodark.py')
    print result.getOutput()
