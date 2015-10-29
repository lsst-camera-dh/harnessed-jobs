#!/usr/bin/env python
from ccsTools import ccsProducer
import time
import subprocess
import commands
import Tkinter
import tkMessageBox
import pyfits
import glob

print "starting widget for checking and starting the CCS apps"


foundjython = False
foundts     = False
foundarchon = False
    
pstr = commands.getstatusoutput('ps -fe')
    
for s in pstr :
    if type(s) is str :
        app = "JythonConsole"
        if app in s :
            foundjython = True
        app = "-app ts"
        if app in s :
            foundts = True
        app = "-app archon"
        if app in s :
            foundarchon = True

if (not (foundjython and foundts and foundarchon)) :
    apptxt = "There are apps missing, please click on this button when\nyou have finished starting them using the widget"
    print apptxt
    top = Tkinter.Tk()
#    def startappsmsg(apptxt):
#        top.stop()
#    A = Tkinter.Button(top, text = apptxt, command = lambda : startappsmsg(apptxt), bg = "red")
    A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "red", font = ("Helvetica",24))
    A.pack()
    top.title('Please start missing CCS apps using the widget that will appear after you click on this button.')
    subprocess.Popen(["gnome-terminal","--geometry=1x1","--working-directory=$CCS_BIN_DIR","--command=/usr/bin/ccsapps"]);
    top.mainloop()
else:
    print "All required CCS apps running"



ccsProducer('preflight_acq', 'ccseopreflight.py')

files = sorted(glob.glob('*.fits'))

#for flat in flats:
hdu1 = pyfits.open(files[0])
hdr1 = hdu1[0].header
exptime1 = hdr1['EXPTIME']
mondiode1 = hdr1['MONDIODE']
filter1 = hdr1['FILTER']

hdu2 = pyfits.open(files[1])
hdr2 = hdu2[0].header
exptime2 = hdr2['EXPTIME']
mondiode2 = hdr2['MONDIODE']
filter2 = hdr2['FILTER']

apptxt = "not OK"
diodecol = "red"
if (abs(mondiode1) > 1.e-10 and abs(mondiode2/mondiode1) > 2.0) :
    apptxt = "OK"
    diodecol = "green"

apptxt = "The diode responses look -- %s -- . Their values are %f for exposure 1 and %f for exposure2." % (apptxt,mondiode1,mondiode2)
print apptxt
top = Tkinter.Tk()
#def startappsmsg(apptxt):
#    top.stop()
#A = Tkinter.Button(top, text = apptxt, command = lambda : startappsmsg(apptxt), bg = diodecol)
A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = diodecol, font = ("Helvetica",16))
A.pack()
top.title('Checking response of PDs')
top.mainloop()
