#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../Make-OGP-Abs-Height-Directories/v0/* | tail -1" % os.getcwd(), shell=True)


theogpabshghtdir = os.path.realpath("%s/abshghtlink/" % ogpdir.strip("\n"))

os.mkdir("AbsHeight")

os.system("cp -r /%s AbsHeight/" % theabshghtdir.strip("/"))

print "looking for link to absolute height files in %s" % (theogpabshghtdir)

abshghtfiles = glob.glob("AbsHeight/*.*")

os.system("rm -rf /cygdrive/c/DATA/Image\ files\ old")
os.system("mv /cygdrive/c/DATA/Image\ files /cygdrive/c/DATA/Image\ files\ old")
os.system("mkdir /cygdrive/c/DATA/Image\ files")

data_products1 = [lcatr.schema.fileref.make(item) for item in abshghtfiles]
results.extend(data_products1)


for item in abshghtfiles :
    print "Archiving AbsHeight file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
