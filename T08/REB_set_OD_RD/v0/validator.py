#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os

results = []

odrdfiles = glob.glob("*.txt")
odrdfiles = odrdfiles + glob.glob("*summary*")

data_products1 = [lcatr.schema.fileref.make(item) for item in odrdfiles]
results.extend(data_products1)


for item in odrdfiles :
    print "Archiving od_rd file - %s" % item



fp = open("REB_od_rd.txt","r");
OD0 = {}
OD1 = {}
OD2 = {}

RD0 = {}
RD1 = {}
RD2 = {}

for ii in range(3) :
    OD0[ii] = "none"
    OD1[ii] = "none"
    OD2[ii] = "none"
    RD0[ii] = "none"
    RD1[ii] = "none"
    RD2[ii] = "none"



for line in fp:
    label = line.split()[0]
    value = line.split()[1]
    ireb = label.split('b')[1]
    iccd = label.split('_')[1]
    
    if "OD" in line.split()[0] :
        if ireb==0 :
            OD0[iccd] = value
        elif ireb==1 :
            OD1[iccd] = value
        else :

            OD2[iccd] = value

    if "RD" in line.split()[0] :
        if ireb==0 :
            RD0[iccd] = value
        elif ireb==1 :
            RD1[iccd] = value
        else :
            RD2[iccd] = value



results.append(lcatr.schema.valid(lcatr.schema.get('REB_OD_RD'),OD0_0=OD0[0], OD1_0=OD1[0], OD2_0=OD2[0],OD0_1=OD0[1], OD1_1=OD1[1], OD2_1=OD2[1],OD0_2=OD0[2], OD1_2=OD1[2], OD2_2=OD2[2],RD0_0=RD0[0], RD1_0=RD1[0], RD2_0=RD2[0],RD0_1=RD0[1], RD1_1=RD1[1], RD2_1=RD2[1],RD0_2=RD0[2], RD1_2=RD1[2], RD2_2=RD2[2]))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


