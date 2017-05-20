#!/usr/bin/env python
from ccsTools import ccsValidator
import siteUtils
import shutil
import lcatr.schema
import glob
import sys

for i in range(20) :
     print "RETEST (N/y)?"
sys.stdout.flush()
answer = raw_input("RETEST (N/y)?")
if "y" in answer.lower() :
     raise Exception("PURPOSELY crashing to allow a retest via retrying the e-Traveler step")


results = []

preflfiles = glob.glob("*.txt")
preflfiles = preflfiles + glob.glob("*summary*")
preflfiles = preflfiles + glob.glob("*png")
preflfiles = preflfiles + glob.glob("*fits")
preflfiles = preflfiles + glob.glob("*/*fits")
preflfiles = preflfiles + glob.glob("*log*")

data_products = [lcatr.schema.fileref.make(item) for item in preflfiles]
results.extend(data_products)

versionfiles = glob.glob("*.txt")
versionfiles = versionfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in versionfiles]
results.extend(data_products1)


for item in versionfiles :
    print "Archiving versions file - %s" % item



fp = open("REB_versions.txt","r");
REBname = {}
REBfirmware = {}
REBSN = {}

REBname[0] = "none"
REBfirmware[0] = "none"
REBSN[0] = "none"

REBname[1] = "none"
REBfirmware[1] = "none"
REBSN[1] = "none"

REBname[2] = "none"
REBfirmware[2] = "none"
REBSN[2] = "none"

id = 0
for line in fp:
    REBname[id] = line.split()[0]
    REBfirmware[id] = line.split()[2]
    REBSN[id] = line.split()[1]
    id = id + 1


results.append(lcatr.schema.valid(lcatr.schema.get('REBVersionsBefore'),REB0name=REBname[0], REB0firmware=REBfirmware[0], REB0SN=REBSN[0],REB1name=REBname[1], REB1firmware=REBfirmware[1], REB1SN=REBSN[1],REB2name=REBname[2], REB2firmware=REBfirmware[2], REB2SN=REBSN[2]))


#results.append(siteUtils.packageVersions())                                                                                                      

lcatr.schema.write_file(results)
lcatr.schema.validate_file()

#ccsValidator('ready_acq')



