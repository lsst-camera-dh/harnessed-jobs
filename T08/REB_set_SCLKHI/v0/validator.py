#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

sclkhifiles = glob.glob("*.txt")
sclkhifiles = sclkhifiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in sclkhifiles]
results.extend(data_products1)


for item in sclkhifiles :
    print "Archiving sclkhi file - %s" % item



fp = open("REB_sclkhi.txt","r");
SCLKHI0 = "none"
SCLKHI1 = "none"
SCLKHI2 = "none"



for line in fp:
    label = line.split()[0]
    sclkhival = line.split()[1]
    ireb = int(label.split('b')[1][0])
    
    if ireb==0 :
        SCLKHI0 = sclkhival
    elif ireb==1 :
        SCLKHI1 = sclkhival
    else :
        SCLKHI2 = sclkhival



results.append(lcatr.schema.valid(lcatr.schema.get('REB_SCLKHI'),SCLKHI0=SCLKHI0, SCLKHI1=SCLKHI1, SCLKHI2=SCLKHI2))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


