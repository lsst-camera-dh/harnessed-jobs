#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../Make-OGP-Abs-Height-Directories/v0/* | tail -1" % os.getcwd(), shell=True)

theogpabshghtdir = os.path.realpath("%s/abshghtlink/" % ogpdir.strip("\n"))
print "looking for links to absolute height files in %s and %s" % (theogpabshghtdir)
abshghtfiles = glob.glob("%s/*.*" % theogpabshghtdir)
for fl in abshghtfiles :
    os.system("chmod 644 %s" % fl)

data_products1 = [lcatr.schema.fileref.make(item) for item in abshghtfiles]
results.extend(data_products1)

for item in abshghtfiles :
    print "Archiving Abshght file - %s" % item

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
