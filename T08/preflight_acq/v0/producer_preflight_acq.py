#!/usr/bin/env python
from ccsTools import ccsProducer
import time
import subprocess
import commands
import Tkinter
import tkMessageBox
import pyfits
import glob
import os
import time
import subprocess

print "starting widget for checking and starting the CCS apps"

#os.system("pkill -f '\-\-app JythonConsole'")
#os.system("pkill -f '\-app RunTS8Subsystem'")
#os.system("pkill -f 'checktsappswidget'")

#time.sleep(10.0)

ccsdir = os.getenv("CCS_BIN_DIR");

#os.system("screen -d -m gnome-terminal --zoom=0.5 --title=JythonConsole --working-directory=%s --command=\"screen -S jython ./JythonConsole\" &" % ccsdir)
#time.sleep(10.0)
#os.system("screen -d -m gnome-terminal --zoom=0.5 --title=ts --working-directory=%s --command=\"screen -S ts8 ./RunTS8Subsystem\" &" % ccsdir)

#time.sleep(30.0)

#os.system("screen -d -m gnome-terminal --geometry=1x1 --working-directory=$CCS_BIN_DIR --command=/usr/bin/ccsapps &")


foundjython = False
foundts8     = False
    
pstr = commands.getstatusoutput('ps -fe')
    
for s in pstr :
    if type(s) is str :
        app = "JythonConsole"
        if app in s :
            foundjython = True

#        app = "-app RunTS8Subsystem"
#        if app in s :
#            foundts8 = True

#if (not (foundjython and foundts8)) :
if (not (foundjython)) :
    apptxt = "There are apps missing, please click on this button when\nyou have finished starting them using the widget"
    print apptxt
    top = Tkinter.Tk()

    A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "red", font = ("Helvetica",24))
    A.pack()
    top.title('Please start missing CCS apps using the widget')

    top.mainloop()
else:
    print "All required CCS apps running"



ccsProducer('preflight_acq', 'ccseopreflight.py')

# make sure all data has arrived
time.sleep(30.)

#files = sorted(glob.glob('*.fits'))
pdfiles = sorted(glob.glob('pd-*.txt'))

fp1 = open(pdfiles[2],"r")
nval =0.
nvalbase=0.
valsum = 0.
valbasesum = 0.
for line in fp1:
    thisval = float(line.split(" ")[1])
    print "measurement = %11.3e" % thisval
    if (thisval < -1e-9) :
#        print "adding signal value"
        valsum  = valsum + thisval
        nval=nval+1.0
        print "nval = %f" % nval
    else :
#        print "adding base value"
        valbasesum  = valbasesum + thisval
        nvalbase=nvalbase+1.0
        print "nvalbase = %f" % nvalbase

nval = max(nval,1.0)
nvalbase = max(nvalbase,1.0)

mondiode1 = valsum / nval - valbasesum / nvalbase
fp1.close()

fp1 = open(pdfiles[3],"r")
nval =0.
nvalbase = 0.
valsum = 0.
valbasesum = 0.
for line in fp1:
    thisval = float(line.split(" ")[1])
    if (thisval < -1e-9) :
        valsum  = valsum + thisval
        nval=nval+1.0
    else :
        valbasesum  = valbasesum + thisval
        nvalbase=nvalbase+1.0

nval = max(nval,1.0)
nvalbase = max(nvalbase,1.0)

mondiode2 = valsum / nval - valbasesum / nvalbase
fp1.close()


#for flat in flats:
#hdu1 = pyfits.open(files[2])
#hdr1 = hdu1[0].header
#exptime1 = hdr1['EXPTIME']
#mondiode1 = hdr1['MONDIODE']
#filter1 = hdr1['FILTER']

#hdu2 = pyfits.open(files[3])
#hdr2 = hdu2[0].header
#exptime2 = hdr2['EXPTIME']
#mondiode2 = hdr2['MONDIODE']
#filter2 = hdr2['FILTER']

#os.system("screen -d -m ds9 -scale datasec yes -scale histequ -mosaicimage iraf %s &" % files[3])
os.system("screen -d -m gnuplot -e \'pdfile=\"%s\"\' /home/ts8prod/lsst/redhat6-x86_64-64bit-gcc44/ccs-utilities/ccs-utilities-20160224/gnuplot/plotpdvals.gp" % pdfiles[3])
os.system("screen -d -m eog pdvals.png")

apptxt = "not OK"
diodecol = "red"
if (abs(mondiode1) > 1.e-10 and abs(mondiode2/mondiode1) > 2.0) :
    apptxt = "OK"
    diodecol = "green"

apptxt = "The diode responses look -- %s -- . Their values are %11.3e for exposure 1 and %11.3e for exposure2." % (apptxt,mondiode1,mondiode2)
print apptxt
top = Tkinter.Tk()

A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = diodecol, font = ("Helvetica",16))
A.pack()
top.title('Checking response of PDs')
top.mainloop()
