#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../Make-OGP-Pin-Directories/v0/* | tail -1" % os.getcwd(), shell=True)


theogppindir = os.path.realpath("%s/pinlink/" % ogpdir.strip("\n"))

os.mkdir("LateralPin")

os.system("cp -r /%s LateralPin/" % theogppindir.strip("/"))

print "looking for link to absolute height files in %s" % (theogppindir)

pinfiles = glob.glob("LateralPin/*.*")

os.system("rm -rf /cygdrive/c/DATA/Image\ files\ old")
os.system("mv /cygdrive/c/DATA/Image\ files /cygdrive/c/DATA/Image\ files\ old")
os.system("mkdir /cygdrive/c/DATA/Image\ files")

data_products1 = [lcatr.schema.fileref.make(item) for item in pinfiles]
results.extend(data_products1)


for item in pinfiles :
    print "Archiving LateralPin file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
