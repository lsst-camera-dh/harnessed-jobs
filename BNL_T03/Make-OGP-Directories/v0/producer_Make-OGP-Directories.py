#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox


ccd = os.environ["LCATR_UNIT_ID"]
topccddir = "/cygdrive/c/DATA/%s" % ccd
print "Creating the top level directory for the CCD at %s" % topccddir
os.mkdir(topccddir)
ccddir = "%s/%s" % (topcddir,time.strftime("%Y%m%d-%H:%M:%S"))
print "Creating dated directory for the CCD at %s" % ccddir
os.mkdir(ccddir)
print "Please setup the OGP MeasureMind application to store results in %s" % cddir

top = Tkinter.Tk()
M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store results in %s" % cddir", bg = "green")
M.pack()
top.title('OGP Dirs Ready')
top.mainloop()
