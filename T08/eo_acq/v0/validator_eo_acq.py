#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import os

os.system("rm -v */*flux*.fits")
os.system("rm -v */*clear*.fits")
#os.system("gzip -v */*.fits")

os.system("cp -p %s ." % sequence_file)

ccsValidator('eo_acq')
