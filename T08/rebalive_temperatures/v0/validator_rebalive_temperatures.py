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

os.system("./rebalive_plots.sh > logpl &")

jobName = "rebalive_temperatures"

results = []

alivefiles = glob.glob("*.txt")
alivefiles = alivefiles + glob.glob("*summary*")
alivefiles = alivefiles + glob.glob("*png")
alivefiles = alivefiles + glob.glob("*log*")

data_products = [lcatr.schema.fileref.make(item) for item in alivefiles]
results.extend(data_products)

statusAssignments = {}

schemaFile = open("%s/%s_runtime.schema.new"%(jobDir,jobName),"w")
schemaFile.write("# -*- python -*-\n")
schemaFile.write("{\n")
schemaFile.write("    \'schema_name\' : \'%s_runtime\',\n"%jobName)
schemaFile.write("    \'schema_version\' : 0,\n")

statusFile = open("rebalive_results.txt")
lnum = 0
for line in statusFile:
    print "line = %s" % line

#    line = line.replace('OK','<font color="green">OK</font>').replace('FAILED','<font color="red">FAILED</font>')

    key = "line%03d" % lnum
    statusAssignments[key] = "%s" % line
    schemaFile.write("    \'%s\' : str,\n" % key)

    lnum = lnum + 1

while (lnum<240):
    key = "line%03d" % lnum
    statusAssignments[key] = "blank"
    schemaFile.write("    \'%s\' : str,\n"%key)

    lnum = lnum + 1


schemaFile.write("}\n")
schemaFile.close()

print "statusAssignments = %s" % statusAssignments

print "jobName = %s" % jobName
lcatr.schema.load("%s/%s_runtime.schema"%(jobDir,jobName))
print "schema = %s" % str(lcatr.schema.get("%s_runtime"%jobName))

#results.append(lcatr.schema.valid(lcatr.schema.get(jobName),
#                                      **statusAssignments))
results.append(lcatr.schema.valid(lcatr.schema.get("%s_runtime"%jobName),
                                      **statusAssignments))

results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


#ccsValidator('rebalive_temperatures')
