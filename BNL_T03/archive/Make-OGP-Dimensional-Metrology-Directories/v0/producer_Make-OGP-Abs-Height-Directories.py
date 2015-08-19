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
abshtdir = "%s/AbshtScan/" % topccddir
print "Creating directory for absht scan results. Location is %s" % abshtdir
#os.mkdir(abshtdir)

abshtdatedir = "%s%s" % (abshtdir,time.strftime("%Y%m%d-%H:%M:%S"))
print "Creating dated absht directory for the CCD at %s" % abshtdatedir
os.makedirs(abshtdatedir)
flatdatedir = "%s%s" % (flatdir,time.strftime("%Y%m%d-%H:%M:%S"))

print "Please setup the OGP MeasureMind application to store results in respective absht scan and flatness directories indicated above"
# leave a link to the location where the files should go
os.system("ln -s %s abshtlink" % abshtdatedir);

#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store<br>absht scan results in %s abshtdatedir<br>and<br>flatness results in %s" % (abshtdatedir,flatdatedir), bg = "green")
#M=Tkinter.Button(top,text="test")
#M.pack()
#top.title('OGP Dirs Ready')
#top.mainloop()
print "Please setup the OGP MeasureMind application to store\nabsht scan results in %s abshtdatedir\nand" % (abshtdatedir)
