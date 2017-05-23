#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import lcatr.schema
import os

results = []

firmupdfiles = glob.glob("*.txt")
firmupdfiles = firmupdfiles + glob.glob("*summary*")
firmupdfiles = firmupdfiles + glob.glob("*.py")
firmupdfiles = firmupdfiles + glob.glob("*.tcl")
firmupdfiles = firmupdfiles + glob.glob("*.bit")

data_products1 = [lcatr.schema.fileref.make(item) for item in firmupdfiles]
results.extend(data_products1)


for item in firmupdfiles :
    print "Archiving file - %s" % item


results.append(siteUtils.packageVersions())



lcatr.schema.write_file(results)
lcatr.schema.validate_file()

