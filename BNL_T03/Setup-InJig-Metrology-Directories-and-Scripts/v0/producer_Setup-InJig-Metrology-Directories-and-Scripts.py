#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox
import time


ccd = os.environ["LCATR_UNIT_ID"]
#/cygdrive/c/Production DATA/ITL-STA3800B-160641/Flatness/150812
topccddir = "/cygdrive/c/Production DATA/%s" % ccd
print "Creating the top level directory for the CCD at %s" % topccddir
#os.mkdir(topccddir)
edgedir = "%s/EdgeScan/" % topccddir
print "Creating directory for edge scan results. Location is %s" % edgedir
#os.mkdir(edgedir)
flatdir = "%s/DimensionMetrology/" % topccddir
print "Creating directory for flatness results. Location is %s" % flatdir
#os.mkdir(flatdir)
edgedatedir = "%s%s" % (edgedir,time.strftime("%Y%m%d-%H:%M:%S"))
print "Creating dated edge directory for the CCD at %s" % edgedatedir
os.makedirs(edgedatedir)
flatdatedir = "%s%s" % (flatdir,time.strftime("%Y%m%d-%H:%M:%S"))
print "Creating dated edge directory for the CCD at %s" % flatdatedir
os.makedirs(flatdatedir)
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
print "Please setup the OGP MeasureMind application to store\nedge scan results in %s edgedatedir\nand\nflatness results in %s" % (edgedatedir,flatdatedir)
print "============================================="
print "Now installing scripts"
tag = os.environ["OGP_SCRIPTS_TAG"]
eohome = os.environ["OGP_SCRIPTS_HOME"]


print "The release of OGP-scripts with tag %s will be installed" % tag
cwd = os.getcwd() 
print "copying old installation of harnessed jobs to a safe place"
os.system("cd %s ; cp -Lrvp harnessed-jobs old-harnessed-jobs-`date +%%F-%%R`" % eohome)
print "moving the original to /tmp"
os.system("cd %s ; cp -Lvrp harnessed-jobs /tmp/ ; mv harnessed-jobs moved-harnessed-jobs" % eohome)
print "downloading tar of new tag"
os.system("cd %s ; wget https://github.com/lsst-camera-dh/harnessed-jobs/archive/%s.tar.gz" % (eohome,tag))
print "untarring"
os.system("cd %s ; tar -vzxf %s.tar.gz" % (eohome,tag))
print "making a link to it"
os.system("cd %s ; ln -s harnessed-jobs-%s harnessed-jobs" % (eohome,tag))

os.system("cd %s" % cwd)

print "The release has been installed."
