#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os
import stat
import Tkinter
import tkMessageBox

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../../*/Run*Setup-InJig-Metrology-Directories-and-Scripts/v0/* | tail -1" % os.getcwd(), shell=True)

theogpedgedir = os.path.realpath("%s/edgelink/" % ogpdir.strip("\n"))
theogpflatdir = os.path.realpath("%s/flatlink/" % ogpdir.strip("\n"))

os.mkdir("DimensionalMetrology")
os.mkdir("EdgeScan")


print "The copy command will be: cp -r /%s DimensionalMetrology/" % theogpflatdir.strip("/")
os.system("cp -r /%s DimensionalMetrology/" % theogpflatdir.strip("/"))

#theogpabshghtdir = os.path.realpath("%s/abshghtlink/" % ogpdir.strip("\n"))
print "Edge scan file will now be moved from C:/DATA/Image  files to %s" % theogpedgedir
os.system("cp -v /cygdrive/c/DATA/Image\ files/* %s" % theogpedgedir)

os.system("cp -r /%s EdgeScan/" % theogpedgedir.strip("/"))


print "looking for links to edge, flatness and absolute height files in %s and %s" % (theogpedgedir,theogpflatdir)
#os.sys("chmod 644 %s/*.*" % theogpedgedir)
#os.sys("chmod 644 %s/*.*" % theogpflatdir)
#edgefiles = glob.glob("%s/*.*" % theogpedgedir)
os.system("chmod 644 */*/*.*")
edgefiles = glob.glob("EdgeScan/*/*.*")
#for fl in edgefiles :
#    os.chmod(fl,stat.S_IRGRP+stat.S_IREAD+stat.S_IWRITE)
#    os.system("chmod 644 %s" % fl)
#flatfiles = glob.glob("%s/*.*" % theogpflatdir)
flatfiles = glob.glob("DimensionalMetrology/*/*.*")
#for fl in flatfiles :
#    os.chmod(fl,stat.S_IRGRP+stat.S_IREAD+stat.S_IWRITE)
#    os.system("chmod 644 %s" % fl)
#abshghtfiles = glob.glob("%s/*.*" % theogpabshghtdir)

os.system("rm -rf /cygdrive/c/DATA/Image\ files\ old")
os.system("mv /cygdrive/c/DATA/Image\ files /cygdrive/c/DATA/Image\ files\ old")
os.system("mkdir /cygdrive/c/DATA/Image\ files")

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

# make a button showing the name that should be used for the output filename
#E2V-CCD250-82-5-G42-14041-08-01_DimMet_20150817-16H23M.DAT
#ccd = os.environ["LCATR_UNIT_ID"]
#dateddir = glob.glob("DimensionalMetrology/*")
#dirdate = dateddir[0].strip("/")
#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please use the following filename as the specification of the output filename\n%s_DimMet_%s.DAT" % (ccd,dirdate), bg = "green")
#M=Tkinter.Button(top,text="filename")
#M.pack()
#top.title('OGP Routine Output Filename')
#top.mainloop()
