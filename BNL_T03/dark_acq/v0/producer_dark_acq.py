#!/usr/bin/env python
import os
from PythonBinding import CcsJythonInterpreter
from CcsSetup import CcsSetup
from siteUtils import jobDirPath, jobName

os.mkdir("bias");

ccs = CcsJythonInterpreter()
setup = CcsSetup('dark_acq.cfg')
result = ccs.syncScriptExecution(jobDirPath('ccseodark.py'), setup(),
                                 verbose=True)
output = open("%s.log" % jobName(), "w")
output.write(result.getOutput())
output.close()
