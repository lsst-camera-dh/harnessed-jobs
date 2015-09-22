#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import lcatr.schema
import os

results = []

warmfiles = glob.glob("*.dat")
warmfiles = warmfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in warmfiles]
results.extend(data_products1)


for item in warmfiles :
    print "Archiving warmup file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
