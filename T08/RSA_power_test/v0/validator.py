#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os
import time

results = []

rsapowerfiles = glob.glob("*.txt")
rsapowerfiles = rsapowerfiles + glob.glob("*summary*")
rsapowerfiles = rsapowerfiles + glob.glob("*log*")
rsapowerfiles = rsapowerfiles + glob.glob("*fits")

data_products1 = [lcatr.schema.fileref.make(item) for item in rsapowerfiles]
results.extend(data_products1)

for item in rsapowerfiles :
    print "Archiving rsa power file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()


