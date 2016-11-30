#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import lcatr.schema
import os

results = []

cntcatchfiles = glob.glob("*.fits")
cntcatchfiles = cntcatchfiles + glob.glob("*.png")
cntcatchfiles = cntcatchfiles + glob.glob("*.txt")
cntcatchfiles = cntcatchfiles + glob.glob("*.log")
cntcatchfiles = cntcatchfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in cntcatchfiles]
results.extend(data_products1)


for item in cntcatchfiles :
    print "Archiving cntcatch file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
