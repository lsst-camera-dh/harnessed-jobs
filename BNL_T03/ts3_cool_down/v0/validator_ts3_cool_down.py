#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import lcatr.schema
import os

results = []

coolfiles = glob.glob("*.dat")
coolfiles = coolfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in coolfiles]
results.extend(data_products1)


for item in coolfiles :
    print "Archiving cool file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()

#ccsValidator('ts3_cool_down_acq')
