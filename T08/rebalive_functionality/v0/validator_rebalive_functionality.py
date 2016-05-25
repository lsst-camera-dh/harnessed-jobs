#!/usr/bin/env python
from ccsTools import ccsValidator
import os
import siteUtils
import shutil
import lcatr.schema

jobDir = siteUtils.getJobDir()

shutil.copy("%s/rebalive_plots.gp" % jobDir ,os.getcwd())
shutil.copy("%s/rebalive_plots.sh" % jobDir ,os.getcwd())

#os.system("./rebalive_plots.sh")


statusAssignments = {}

statusFile = open("rebalive_results.txt")
for line in statusFile:
    print "line = %s" % line
    values = line.split("|")
    statusAssignments[values[0]] = values[1].strip("[|]").strip(",")
    
print "statusAssignments = %s" % statusAssignments

jobName = "rebalive_functionality"

print "jobName = %s" % jobName
print "schema = %s" % str(lcatr.schema.get(jobName))

results = []

results.append(lcatr.schema.valid(lcatr.schema.get(jobName),
                                      **statusAssignments))

results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


#ccsValidator('rebalive_functionality')
