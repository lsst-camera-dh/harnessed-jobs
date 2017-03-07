#!/usr/bin/env python
#from ccsTools import ccsValidator
import glob
import os
import lcatr.schema

results = []

datfile = glob.glob("*.csv")[0]

os.system("grep \"^#\" %s > temp.dat" % datfile)
os.system("grep -v \"^#\" %s >> temp.dat" % datfile)
os.system("mv temp.dat %s" % datfile)

ingfiles = glob.glob("*.log")
ingfiles.append(datfile)

data_products = [lcatr.schema.fileref.make(item) for item in ingfiles]
results.extend(data_products)

#os.system("rm Cold-Measurement.log")
#ccsValidator('Cold-Measurement')
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
