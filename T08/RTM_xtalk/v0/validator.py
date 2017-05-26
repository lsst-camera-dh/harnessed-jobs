#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os
import time

results = []

rtmxtalkfiles = glob.glob("*.txt")
rtmxtalkfiles = rtmxtalkfiles + glob.glob("*summary*")
rtmxtalkfiles = rtmxtalkfiles + glob.glob("*log*")
rtmxtalkfiles = rtmxtalkfiles + glob.glob("*fits")
rtmxtalkfiles = rtmxtalkfiles + glob.glob("S*/*fits")

data_products1 = [lcatr.schema.fileref.make(item) for item in rtmxtalkfiles]
results.extend(data_products1)

for item in rtmxtalkfiles :
    print "Archiving rtm xtalk file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
