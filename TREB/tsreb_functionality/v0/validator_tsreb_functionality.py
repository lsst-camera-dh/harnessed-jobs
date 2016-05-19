#!/usr/bin/env python
import glob
import lcatr.schema
import os
import siteUtils

results = []

files = glob.glob('*.*')    
data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

for item in files :
    print "Archiving file - %s" % item

lcatr.schema.write_file(results)
lcatr.schema.validate_file()

