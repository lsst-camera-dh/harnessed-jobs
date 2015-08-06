#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
# cannot access siteUtils on this machine so ...

ogpdir = subprocess.check_output("ls -rtd %s/../../../Make-OGP-Abs-Height-Directories/v0/* | tail -1" % os.getcwd(), shell=True)

theogpabshtdir = os.path.realpath("%s/abshtlink/" % ogpdir.strip("\n"))

print "looking for links to absolute height files in %s" % (theogpabshtdir)
abshtfiles = glob.glob("%s/*.*" % theogpabshtdir)

#files = glob.glob('*.*')    
data_products1 = [lcatr.schema.fileref.make(item) for item in abshtfiles]
results.extend(data_products1)

for item in abshtfiles :
    print "Archiving Absht file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
