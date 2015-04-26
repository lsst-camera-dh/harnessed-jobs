import os
from PythonBinding import CcsJythonInterpreter
from CcsSetup import CcsSetup
from siteUtils import jobDirPath

def ccsProduction(jobName, ccsScript, makeBiasDir=True, verbose=True):
    if makeBiasDir:
        os.mkdir("bias")

    ccs = CcsJythonInterpreter()
    setup = CcsSetup('%s.cfg' % jobName)
    result = ccs.syncScriptExecution(jobDirPath(ccsScript), setup(),
                                     verbose=verbose)
    output = open("%s.log" % jobName, "w")
    output.write(result.getOutput())
    output.close()
