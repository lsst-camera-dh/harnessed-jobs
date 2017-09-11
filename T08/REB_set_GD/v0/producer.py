#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(5) :
    print " "

print "Enter the setting for GD - "
sys.stdout.flush()
GD = raw_input(" ")

fp = open("gd_settings.txt","w");
fp.write("GD %f\n" % float(GD))
fp.close()


ccsProducer('REB_set_GD', 'ccseo_set_gd.py')
