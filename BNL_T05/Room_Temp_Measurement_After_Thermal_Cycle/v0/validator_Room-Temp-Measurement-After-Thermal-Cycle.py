#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import os

datfile = glob.glob("*.dat")[0]
os.system("grep \"^#\" %s > temp.dat" % datfile)
os.system("grep -v \"^#\" %s >> temp.dat" % datfile)
os.system("mv temp.dat %s" % datfile)

ccsValidator('Room-Temp-Measurement-After-Thermal-Cycle')
