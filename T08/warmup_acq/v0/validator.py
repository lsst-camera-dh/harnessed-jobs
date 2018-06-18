#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os
import time

results = []

warmupfiles = glob.glob("*.txt")
warmupfiles = warmupfiles + glob.glob("*summary*")
warmupfiles = warmupfiles + glob.glob("*log*")
warmupfiles = warmupfiles + glob.glob("*fits")

data_products1 = [lcatr.schema.fileref.make(item) for item in warmupfiles]
results.extend(data_products1)

for item in warmupfiles :
    print "Archiving warmups file - %s" % item

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


