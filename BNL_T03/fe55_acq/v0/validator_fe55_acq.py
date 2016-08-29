#!/usr/bin/env python
from ccsTools import ccsValidator

import os
import siteUtils
import shutil
import lcatr.schema
import glob
import hdrtools

jobDir = siteUtils.getJobDir()

jobName = "fe55_acq"

results = []

statusAssignments = {}

statusflags = ['stat','teststand_version','teststand_revision','archon_version','archon_revision']

updateschema = False

if updateschema:
    schemaFile = open("%s/%s_runtime.schema"%(jobDir,jobName),"w")
    schemaFile.write("# -*- python -*-\n")
    schemaFile.write("{\n")
    schemaFile.write("    \'schema_name\' : \'%s_runtime\',\n"%jobName)
    schemaFile.write("    \'schema_version\' : 0,\n")
else:
    statoutFile = open("status.out","append")

statusFile = open("bias-voltages.out")
for line in statusFile:
    print "line = %s" % line
    values = line.split("|")
    val = values[1].strip("[|]").strip(",")
    aa = values[0]
    if updateschema:
#    if not "device" in aa :
#        schemaFile.write("    \'%s\' : float,\n"%values[0])
#        if "fail" in val :
#            val = -9999999.
#    else :
        schemaFile.write("    \'%s\' : str,\n"%values[0])
    else:
        statoutFile.write(val)

    statusAssignments[values[0]] = val
    statusflags.append(values[0])

if updateschema:
    schemaFile.write("}\n")
    schemaFile.close()
else:
    statoutFile.close()

print "statusAssignments = %s" % statusAssignments
print "statusflags = %s" % statusflags

print "jobName = %s" % jobName
if updateschema:
    lcatr.schema.load("%s/%s_runtime.schema"%(jobDir,jobName))
    print "schema = %s" % str(lcatr.schema.get("%s_runtime"%jobName))

#results.append(lcatr.schema.valid(lcatr.schema.get(jobName),
#                                      **statusAssignments))
if updateschema:
    results.append(lcatr.schema.valid(lcatr.schema.get("%s_runtime"%jobName),
                                      **statusAssignments))

    results.append(siteUtils.packageVersions())

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()

    try:
        hdrtools.updateFitsHeaders('acqfilelist')
    except IOError:
        pass
else :
    ccsValidator('fe55_acq','acqfilelist',statusflags)
