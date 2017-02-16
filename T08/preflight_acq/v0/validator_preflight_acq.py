#!/usr/bin/env python
from ccsTools import ccsValidator
import siteUtils
import shutil
import lcatr.schema
import glob

print "RETEST (N/y)?"
answer = raw_input("RETEST (N/y)?")
if "y" in answer.lower() :
     raise Exception("PURPOSELY crashing to allow a retest via retrying the e-Traveler step")


results = []

preflfiles = glob.glob("*.txt")
preflfiles = preflfiles + glob.glob("*summary*")
preflfiles = preflfiles + glob.glob("*png")
preflfiles = preflfiles + glob.glob("*log*")

data_products = [lcatr.schema.fileref.make(item) for item in preflfiles]
results.extend(data_products)

#results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()

#ccsValidator('preflight_acq')
