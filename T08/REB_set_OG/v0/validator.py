#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

ogfiles = glob.glob("*.txt")
ogfiles = ogfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in ogfiles]
results.extend(data_products1)


for item in ogfiles :
    print "Archiving og file - %s" % item



fp = open("REB_og.txt","r");
OG0 = {}
OG1 = {}
OG2 = {}

for ii in range(3) :
    OG0[ii] = "none"
    OG1[ii] = "none"
    OG2[ii] = "none"



for line in fp:
    label = line.split()[0]
    ogval = line.split()[1]
    ireb = int(label.split('b')[1][0])
    iccd = int(label.split('_')[1][0])
    
    if ireb==0 :
        OG0[iccd] = ogval
    elif ireb==1 :
        OG1[iccd] = ogval
    else :
        OG2[iccd] = ogval



results.append(lcatr.schema.valid(lcatr.schema.get('REB_OG'),OG0_0=OG0[0], OG1_0=OG1[0], OG2_0=OG2[0],OG0_1=OG0[1], OG1_1=OG1[1], OG2_1=OG2[1],OG0_2=OG0[2], OG1_2=OG1[2], OG2_2=OG2[2]))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


