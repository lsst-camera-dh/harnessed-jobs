#!/usr/bin/env python
from ccsTools import ccsValidator

#ccsValidator('mono_calib_acq')
import glob
import siteUtils
import lcatr.schema
import os
import time

results = []

pdfiles = glob.glob("*.txt")
pdfiles = pdfiles + glob.glob("*summary*")
pdfiles = pdfiles + glob.glob("*log*")
pdfiles = pdfiles + glob.glob("*fits")

data_products1 = [lcatr.schema.fileref.make(item) for item in pdfiles]
results.extend(data_products1)

for item in pdfiles :
    print "Archiving pds file - %s" % item



lcatr.schema.write_file(results)
lcatr.schema.validate_file()
