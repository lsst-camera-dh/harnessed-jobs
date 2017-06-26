#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(5) :
    print " "

print "Enter the setting for CSGATE - "
sys.stdout.flush()
CSGATE = raw_input(" ")

fp = open("csgate_settings.txt","w");
fp.write("CSGATE %f\n" % float(CSGATE))
fp.close()


ccsProducer('REB_set_CSGATE', 'ccseo_set_csgate.py')
