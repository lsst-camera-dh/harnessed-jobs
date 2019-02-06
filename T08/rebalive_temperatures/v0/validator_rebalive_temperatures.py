#!/usr/bin/env python
from ccsTools import ccsValidator
import os
import siteUtils
import shutil
import lcatr.schema
import glob

jobDir = siteUtils.getJobDir()

shutil.copy("%s/rebalive_plots.gp" % jobDir ,os.getcwd())
shutil.copy("%s/rebalive_plots.sh" % jobDir ,os.getcwd())
shutil.copy("%s/plotchans.list" % jobDir ,os.getcwd())
shutil.copy("%s/ccs_trending.py" % jobDir ,os.getcwd())
shutil.copy("%s/genpoweringreport.py" % jobDir ,os.getcwd())
shutil.copy("%s/ts8power_quantities.cfg" % jobDir ,os.getcwd())

#os.system("./rebalive_plots.sh > logpl &")
os.system("python genpoweringreport.py > logpl")

jobName = "rebalive_temperatures"

results = []

alivefiles = glob.glob("*.txt")
alivefiles = alivefiles + glob.glob("*summary*")
alivefiles = alivefiles + glob.glob("*png")
alivefiles = alivefiles + glob.glob("*log*")

data_products = [lcatr.schema.fileref.make(item) for item in alivefiles]
results.extend(data_products)

statusAssignments = {}

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
