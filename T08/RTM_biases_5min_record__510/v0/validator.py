#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import siteUtils
import lcatr.schema
import os
import time

results = []

thermalfiles = glob.glob("*.txt")
thermalfiles = thermalfiles + glob.glob("*summary*")
thermalfiles = thermalfiles + glob.glob("*log*")
thermalfiles = thermalfiles + glob.glob("*fits")
thermalfiles = thermalfiles + glob.glob("*png")

data_products1 = [lcatr.schema.fileref.make(item) for item in thermalfiles]
results.extend(data_products1)

for item in thermalfiles :
    print "Archiving thermals file - %s" % item


if True :
    fp = open("status.out","r");
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
    
    status = ""
    id = 0
    iln = 0
    for line in fp:
        if (iln==0) :
            status = line
        else :
            REBname[id] = line.split()[0]
            REBfirmware[id] = line.split()[2]
            REBSN[id] = line.split()[1]
            id = id + 1
        iln = iln + 1

    tm = str(time.time())

    results.append(lcatr.schema.valid(lcatr.schema.get('thermInfo'),status=status,time=tm,REB0name=REBname[0], REB0firmware=REBfirmware[0], REB0SN=REBSN[0],REB1name=REBname[1], REB1firmware=REBfirmware[1], REB1SN=REBSN[1],REB2name=REBname[2], REB2firmware=REBfirmware[2], REB2SN=REBSN[2]))

#results.append(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


