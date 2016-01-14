#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox
import time


#ogpscriptname = "CCDb\_Flatness\_Edge\_scan\_new\_jig\_robust.RTN"
ogpscriptname1 = "ITL\_Flatness.RTN"
ogpscriptname2 = "ITL\_EdgeScan.RTN"

ccd = os.environ["LCATR_UNIT_ID"]

topccddir = "/cygdrive/c/Production_DATA/%s" % ccd
print "Creating the top level directory for the CCD at %s" % topccddir

edgedir = "%s/EdgeScan/" % topccddir
print "Creating directory for edge scan results. Location is %s" % edgedir

flatdir = "%s/Flatness/" % topccddir
print "Creating directory for flatness results. Location is %s" % flatdir

tm = time.strftime("%Y%m%d-%HH%MM")

edgedatedir = "%s%s" % (edgedir,tm)
print "Creating dated edge directory for the CCD at %s" % edgedatedir
os.makedirs(edgedatedir)
os.system("chmod 777 %s" %  edgedatedir)
flatdatedir = "%s%s" % (flatdir,tm)
print "Creating dated edge directory for the CCD at %s" % flatdatedir
os.makedirs(flatdatedir)
os.system("chmod 777 %s" %  flatdatedir)
print "Please setup the OGP MeasureMind application to store results in respective edge scan and flatness directories indicated above"

# leave a link to the location where the files should go
print "Making links to the data directories in %s" % os.getcwd()
os.system("ln -s %s edgelink" % edgedatedir);
os.system("ln -s %s flatlink" % flatdatedir);
os.system("ls -lrt")

#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store<br>edge scan results in %s edgedatedir<br>and<br>flatness results in %s" % (edgedatedir,flatdatedir), bg = "green")
#M=Tkinter.Button(top,text="test")
#M.pack()
#top.title('OGP Dirs Ready')
#top.mainloop()

print "Please setup the OGP MeasureMind application to store\nedge scan results in %s \nand\nflatness results in %s" % (edgedatedir,flatdatedir)
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

os.system("cp -vp %s/OGP-scripts/Production\ routines/%s %s" % (ogpscriptshome,ogpscriptname1,flatdatedir))
os.system("cp -vp %s/OGP-scripts/Production\ routines/%s %s" % (ogpscriptshome,ogpscriptname2,edgedatedir))

os.system("cd %s" % cwd)

print "The OGP acquisition and analysis scripts have been installed."
rtnnam = "%s_Flat_%s.DAT" % (ccd,tm)
#tkMessageBox.showinfo("OGP Routine Data Output Filename", rtnnam)
#subprocess.Popen(["/home/LSSTuser/lsst/showfl.py",rtnnam]);

print "======================================="
print "OGP Routine Data Output Filename: %s" % rtnnam
print "======================================="
