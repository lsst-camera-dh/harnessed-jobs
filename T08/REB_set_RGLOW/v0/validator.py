#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

rglowfiles = glob.glob("*.txt")
rglowfiles = rglowfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in rglowfiles]
results.extend(data_products1)


for item in rglowfiles :
    print "Archiving rglow file - %s" % item



fp = open("REB_rglow.txt","r");
RGLOW0 = "none"
RGLOW1 = "none"
RGLOW2 = "none"



for line in fp:
    label = line.split()[0]
    rglowval = line.split()[1]
    ireb = int(label.split('b')[1][0])
    
    if ireb==0 :
        RGLOW0 = rglowval
    elif ireb==1 :
        RGLOW1 = rglowval
    else :
        RGLOW2 = rglowval



results.append(lcatr.schema.valid(lcatr.schema.get('REB_RGLOW'),RGLOW0=RGLOW0, RGLOW1=RGLOW1, RGLOW2=RGLOW2))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


