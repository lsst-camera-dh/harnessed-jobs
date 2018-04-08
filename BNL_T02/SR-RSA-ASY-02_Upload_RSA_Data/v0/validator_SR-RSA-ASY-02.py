#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os
import Tkinter
import tkMessageBox
#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../../*/SR-RSA-ASY-02_Make_RSA_Directories/v0/* | tail -1" % os.getcwd(), shell=True)


theogprsadir = os.path.realpath("%s/rsalink/" % ogpdir.strip("\n"))

os.mkdir("RSA")

os.system("cp -r /%s RSA/" % theogprsadir.strip("/"))

print "looking for link to absolute height files in %s" % (theogprsadir)

os.system("chmod -R 644 .")
rsafiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk("RSA/") for f in filenames]

os.system("rm -rf /cygdrive/c/DATA/Image\ files\ old")
os.system("mv /cygdrive/c/DATA/Image\ files /cygdrive/c/DATA/Image\ files\ old")
os.system("mkdir /cygdrive/c/DATA/Image\ files")

data_products1 = [lcatr.schema.fileref.make(item) for item in rsafiles]
results.extend(data_products1)


for item in rsafiles :
    print "Archiving RSA file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()
