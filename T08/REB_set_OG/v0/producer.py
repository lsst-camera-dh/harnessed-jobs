#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(5) :
    print " "

print "Enter the setting for OG - "
sys.stdout.flush()
OG = raw_input(" ")

fp = open("og_settings.txt","w");
fp.write("OG %f\n" % float(OG))
fp.close()


ccsProducer('REB_set_OG', 'ccseo_set_og.py')
