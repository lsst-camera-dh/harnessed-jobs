#!/usr/bin/env python
import os
import sys
from PythonBinding import CcsJythonInterpreter
from CcsSetup import CcsSetup
from siteUtils import jobDirPath, jobName

os.mkdir("bias");

ccs = CcsJythonInterpreter()
setup = CcsSetup('fe55_acq.cfg')
result = ccs.syncScriptExecution(jobDirPath('ccseofe55.py'), setup(),
                                 verbose=True)
log = result.getOutput()
output = open("%s.log" % jobName(), "w")
output.write(log)
output.close()

