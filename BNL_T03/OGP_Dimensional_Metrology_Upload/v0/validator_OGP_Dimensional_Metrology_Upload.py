#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../Setup-InJig-Metrology-Directories-and-Scripts/v0/* | tail -1" % os.getcwd(), shell=True)

theogpedgedir = os.path.realpath("%s/edgelink/" % ogpdir.strip("\n"))
theogpflatdir = os.path.realpath("%s/flatlink/" % ogpdir.strip("\n"))
#theogpabshghtdir = os.path.realpath("%s/abshghtlink/" % ogpdir.strip("\n"))
print "looking for links to edge, flatness and absolute height files in %s and %s" % (theogpedgedir,theogpflatdir)
os.sys("chmod 644 %s/*.*" % theogpedgedir)
os.sys("chmod 644 %s/*.*" % theogpflatdir)
edgefiles = glob.glob("%s/*.*" % theogpedgedir)
flatfiles = glob.glob("%s/*.*" % theogpflatdir)
#abshghtfiles = glob.glob("%s/*.*" % theogpabshghtdir)

#files = glob.glob('*.*')
data_products1 = [lcatr.schema.fileref.make(item) for item in edgefiles]
results.extend(data_products1)
data_products2 = [lcatr.schema.fileref.make(item) for item in flatfiles]
results.extend(data_products2)
#data_products3 = [lcatr.schema.fileref.make(item) for item in abshghtfiles]
#results.extend(data_products3)

for item in edgefiles :
    print "Archiving Edge file - %s" % item
for item in flatfiles :
    print "Archiving Flatness file - %s" % item
#for item in abshghtfiles :
#    print "Archiving Absolute Height file - %s" % item

lcatr.schema.write_file(results)
lcatr.schema.validate_file()