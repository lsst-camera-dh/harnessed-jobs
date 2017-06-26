#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(5) :
    print " "

print "Enter the setting for SCLKHI - "
sys.stdout.flush()
SCLKHI = raw_input(" ")

fp = open("sclkhi_settings.txt","w");
fp.write("SCLKHI %f\n" % float(SCLKHI))
fp.close()


ccsProducer('REB_set_SCLKHI', 'ccseo_set_sclkhi.py')
