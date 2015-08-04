#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox
import time


ccd = os.environ["LCATR_UNIT_ID"]
topccddir = "/cygdrive/c/DATA/%s" % ccd
print "Creating the top level directory for the CCD at %s" % topccddir
#os.mkdir(topccddir)
edgedir = "%s/EdgeScan/" % topccddir
print "Creating directory for edge scan results. Location is %s" % edgedir
#os.mkdir(edgedir)
flatdir = "%s/Flatness/" % topccddir
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
os.system("ln -s %s edgelink" % edgedatedir);
os.system("ln -s %s flatlink" % flatdatedir);

#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store<br>edge scan results in %s edgedatedir<br>and<br>flatness results in %s" % (edgedatedir,flatdatedir), bg = "green")
#M=Tkinter.Button(top,text="test")
#M.pack()
#top.title('OGP Dirs Ready')
#top.mainloop()
print "Please setup the OGP MeasureMind application to store\nedge scan results in %s edgedatedir\nand\nflatness results in %s" % (edgedatedir,flatdatedir)
