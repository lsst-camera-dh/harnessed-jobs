#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

csgatefiles = glob.glob("*.txt")
csgatefiles = csgatefiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in csgatefiles]
results.extend(data_products1)


for item in csgatefiles :
    print "Archiving csgate file - %s" % item



fp = open("REB_csgate.txt","r");
CCDI0 = {}
CCDI1 = {}
CCDI2 = {}

for ii in range(3) :
    CCDI0[ii] = "none"
    CCDI1[ii] = "none"
    CCDI2[ii] = "none"



for line in fp:
    label = line.split()[0]
    ccdival = line.split()[1]
    ireb = int(label.split('b')[1][0])
    iccd = int(label.split('_')[1][0])
    
    if ireb==0 :
        CCDI0[iccd] = ccdival
    elif ireb==1 :
        CCDI1[iccd] = ccdival
    else :
        CCDI2[iccd] = ccdival



results.append(lcatr.schema.valid(lcatr.schema.get('REB_CSGATE'),CCDI0_0=CCDI0[0], CCDI1_0=CCDI1[0], CCDI2_0=CCDI2[0],CCDI0_1=CCDI0[1], CCDI1_1=CCDI1[1], CCDI2_1=CCDI2[1],CCDI0_2=CCDI0[2], CCDI1_2=CCDI1[2], CCDI2_2=CCDI2[2]))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


