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

if '_RGLOW_' in jobname :
    parts = jobname.split('_')
    np = len(parts)
    sRGLOW = parts[np-2]+'.'+parts[np-1]
    print "sRGLOW = ",sRGLOW
    RGLOW = float(sRGLOW)
    if 'minus' in parts[np-3] :
        RGLOW = -RGLOW
else :
    print "Enter the setting for RGLOW - "
    sys.stdout.flush()
    RGLOW = raw_input(" ")

fp = open("rglow_settings.txt","w");
fp.write("RGLOW %f\n" % float(RGLOW))
fp.close()


ccsProducer('REB_set_RGLOW', 'ccseo_set_rglow.py')
