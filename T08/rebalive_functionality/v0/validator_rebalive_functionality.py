#!/usr/bin/env python
from ccsTools import ccsValidator
import os
import siteUtils
import shutil

jobDir = siteUtils.getJobDir()

shutil.copy("%s/rebalive_plots.gp" % jobDir ,os.getcwd())
shutil.copy("%s/rebalive_plots.sh" % jobDir ,os.getcwd())

os.system("./rebalive_plots.sh")

ccsValidator('rebalive_functionality')
