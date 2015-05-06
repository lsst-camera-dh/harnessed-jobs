"""
PythonBinding simulator for executing ccsTools.ccsProducer(...).
Sensor data for each test are copied from a directory containing a
simulated (or real) dataset for each CCS data acquistion script, which
have names "ccseo<dataset_name>.py"
"""
import os
import subprocess

class AcqSim(object):
    datasets = 'fe55 dark flat qe sflat ppump xtalk fluxcal'.split()
    def __init__(self, rootdir):
        self.rootdir = rootdir
    def getData(self, dataset):
        if dataset not in self.datasets:
            raise RuntimeError("Invalid dataset name.")
        command = "cp %s ." % os.path.join(self.rootdir, dataset, '*')
        subprocess.call(command, shell=True)

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
        self.acq.getData(dataset)
        return CcsResult(filename)

if __name__ is '__main__':
    os.environ['SIMDIR'] = '../data'
    ccs = CcsJythonInterpreter()

    result = ccs.syncScriptExecution('ccseofe55.py')
    print result.getOutput()

    result = ccs.syncScriptExecution('ccseodark.py')
    print result.getOutput()
