#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

gdfiles = glob.glob("*.txt")
gdfiles = gdfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in gdfiles]
results.extend(data_products1)


for item in gdfiles :
    print "Archiving gd file - %s" % item



fp = open("REB_gd.txt","r");
GD0 = {}
GD1 = {}
GD2 = {}

for ii in range(3) :
    GD0[ii] = "none"
    GD1[ii] = "none"
    GD2[ii] = "none"



for line in fp:
    label = line.split()[0]
    gdval = line.split()[1]
    ireb = int(label.split('b')[1][0])
    iccd = int(label.split('_')[1][0])
    
    if ireb==0 :
        GD0[iccd] = gdval
    elif ireb==1 :
        GD1[iccd] = gdval
    else :
        GD2[iccd] = gdval



results.append(lcatr.schema.valid(lcatr.schema.get('REB_GD'),GD0_0=GD0[0], GD1_0=GD1[0], GD2_0=GD2[0],GD0_1=GD0[1], GD1_1=GD1[1], GD2_1=GD2[1],GD0_2=GD0[2], GD1_2=GD1[2], GD2_2=GD2[2]))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


