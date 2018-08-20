#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys
import siteUtils

for i in range(5) :
    print " "

jobname = siteUtils.getJobName()


if '_OG_' in jobname :
    parts = jobname.split('_')
    np = len(parts)
    sOG = parts[np-2]+'.'+parts[np-1]
    print "sOG = ",sOG
    OG = float(sOG)
    if 'minus' in parts[np-3] :
        OG = -OG
else :
    print "Enter the setting for OG - "
    sys.stdout.flush()
    OG = raw_input(" ")

fp = open("og_settings.txt","w");
fp.write("OG %f\n" % float(OG))
fp.close()


ccsProducer('REB_set_OG', 'ccseo_set_og.py')
