#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(5) :
    print " "

print "Enter the setting for OD - "
sys.stdout.flush()
OD = raw_input(" ")

print "\n\nEnter the setting for RD - "
sys.stdout.flush()
RD = raw_input("  ")

fp = open("od_rd_settings.txt","w");
fp.write("OD %f\n" % float(OD))
fp.write("RD %f\n" % float(RD))
fp.close()


ccsProducer('REB_set_OD_RD', 'ccseo_set_od_rd.py')
