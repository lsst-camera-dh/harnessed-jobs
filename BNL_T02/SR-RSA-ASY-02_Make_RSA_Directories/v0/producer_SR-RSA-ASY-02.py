#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox
import time


ogpscriptname = ""

ccd = os.environ["LCATR_UNIT_ID"]


topccddir = "/dev/null"
rsadir = "/dev/null"
rsadatedir = "/dev/null"

omt = os.getenv("OGP_MANUAL_TIME")
if omt is None :
    tm = time.strftime("%Y%m%d-%HH%MM")
    topccddir = "/cygdrive/c/Production_DATA/%s" % ccd
    print "Creating the top level directory for the CCD at %s" % topccddir
    rsadir = "%s/RSA/" % topccddir
    print "Creating directory for the RSA results. The location is %s" % rsadir
    rsadatedir = "%s%s" % (rsadir,tm)
    print "Creating dated RSA directory for the CCD at %s" % rsadatedir
    os.makedirs(rsadatedir)
    print "Please setup the OGP MeasureMind application to store results in the respective RSA directory indicated above"
else :
    print "!!! AN OGP MANUAL TIME HAS BEEN SPECIFIED !!!"
    tm = omt
    topccddir = "/cygdrive/c/Production_DATA_manual/%s" % ccd
    rsadir = "%s/RSA/" % topccddir
    rsadatedir = "%s%s" % (rsadir,tm)
    print "The name for the RSA directory will be %s" % rsadatedir
    print "Will assume data already in the RSA directory indicated above"
    os.unsetenv("OGP_MANUAL_TIME")

os.system("chmod 777 %s" %  rsadatedir)


# leave a link to the location where the files should go
print "Making links to the data directories in %s" % os.getcwd()
os.system("ln -s %s rsalink" % rsadatedir);
os.system("ls -lrt")

#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store<br>edge scan results in %s edgedatedir<br>and<br>RSA results in %s" % (edgedatedir,rsadatedir), bg = "green")
#M=Tkinter.Button(top,text="test")
#M.pack()
#top.title('OGP Dirs Ready')
#top.mainloop()

print "Please setup the OGP MeasureMind application to store RSA results in %s" % (rsadatedir)
print "============================================="
print "Now installing scripts"
tag = os.environ["OGP_SCRIPTS_TAG"]
ogpscriptshome = os.environ["OGP_SCRIPTS_HOME"]


print "The release of OGP-scripts with tag %s will be installed" % tag
cwd = os.getcwd() 
print "copying old installation of OGP scripts to a safe place"
os.system("cd %s ; cp -Lrvp OGP-scripts old-OGP-scripts-`date +%%F-%%R`" % ogpscriptshome)
print "moving the original to /tmp"
os.system("cd %s ; cp -Lvrp OGP-scripts /tmp/ ; mv OGP-scripts moved-OGP-scripts" % ogpscriptshome)
print "downloading tar of new tag"
os.system("cd %s ; wget https://github.com/lsst-camera-dh/OGP-scripts/archive/%s.tar.gz" % (ogpscriptshome,tag))
print "untarring"
os.system("cd %s ; tar -vzxf %s.tar.gz" % (ogpscriptshome,tag))
print "making a link to it"
os.system("cd %s ; ln -s OGP-scripts-%s OGP-scripts" % (ogpscriptshome,tag))

versionsFile = open("%s/OGP-scripts/Production routines/RTN_versions.txt" % ogpscriptshome )
for line in versionsFile:
    values = line.split("|")
    if "RSA" in values[0] :
        ogpscriptname = values[0]
        print "For RSA , using - %s" % line



os.system("cp -vp %s/OGP-scripts/Production\ routines/%s %s" % (ogpscriptshome,ogpscriptname,rsadatedir))

os.system("cd %s" % cwd)

print "The OGP acquisition and analysis scripts have been installed."

#datnam = "%s_AbsZ_%s.DAT" % (ccd,tm)

print "======================================="
#print "OGP Routine Data Output Filename: %s" % datnam
print "           The End"
print "======================================="
