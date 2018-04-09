#!/usr/bin/env python
from ccsTools import ccsValidator
import os
import siteUtils
import shutil
import lcatr.schema
import glob
import pyfits
import sys
import numpy
import numpy.random
import Tkinter

jobDir = siteUtils.getJobDir()

jobName = "scan_plots"






results = []

scanfiles = glob.glob("*.txt")
scanfiles = scanfiles + glob.glob("*summary*")
scanfiles = scanfiles + glob.glob("*png")
scanfiles = scanfiles + glob.glob("*log*")
scanfiles = scanfiles + glob.glob("*fits")

data_products = [lcatr.schema.fileref.make(item) for item in scanfiles]
results.extend(data_products)

statusAssignments = {}


print "jobName = %s" % jobName
lcatr.schema.load("%s/%s_runtime.schema"%(jobDir,jobName))
print "schema = %s" % str(lcatr.schema.get("%s_runtime"%jobName))


#results.append(lcatr.schema.valid(lcatr.schema.get("%s_runtime"%jobName),
#                                      **statusAssignments))

#results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


