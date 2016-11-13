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

# see if the status file is there thus indicating successful completion of the ccs script
fp = open("status.out","r");

#ccsValidator('ts8_cool_down_acq')
