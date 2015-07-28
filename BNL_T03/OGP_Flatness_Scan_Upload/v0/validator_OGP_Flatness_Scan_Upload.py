#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os

#import siteUtils

results = []
#ccd = os.environ["LCATR_UNIT_ID"]
#topccddir = "/cygdrive/c/DATA/%s" % ccd
#ccddir = "%s/%s" % (topcddir,time.strftime("%Y%m%d-%H:%M:%S"))

#os.system("cp -vp %s/* ." % cddir)
#os.system("chmod 644 *.*")

# edge scan files
#files1 = siteUtils.dependency_glob('edgelink/*.*',
#                                  jobname=siteUtils.getProcessName('Make-OGP-Directories'),
#                                  description='OGP result files:')

# flatness files
#files2 = siteUtils.dependency_glob('flatlink/*.*',
#                                  jobname=siteUtils.getProcessName('Make-OGP-Directories'),
#                                  description='OGP result files:')

# cannot access siteUtils on this machine so ...

ogpdir = subprocess.check_output("ls -rtd %s/../../../Make-OGP-Directories/v0/* | tail -1" % os.getcwd(), shell=True)

theogpedgedir = os.path.realpath("%s/edgelink/" % ogpdir.strip("\n"))
theogpflatdir = os.path.realpath("%s/flatlink/" % ogpdir.strip("\n"))
print "looking for links to edge and flatness files in %s and %s" % (theogpedgedir,theogpflatdir)
edgefiles = glob.glob("%s/*.*" % theogpedgedir)
flatfiles = glob.glob("%s/*.*" % theogpflatdir)

#files = glob.glob('*.*')    
data_products1 = [lcatr.schema.fileref.make(item) for item in edgefiles]
results.extend(data_products1)
data_products2 = [lcatr.schema.fileref.make(item) for item in flatfiles]
results.extend(data_products2)

for item in edgefiles :
    print "Archiving Edge file - %s" % item
for item in flatfiles :
    print "Archiving Flatness file - %s" % item

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
