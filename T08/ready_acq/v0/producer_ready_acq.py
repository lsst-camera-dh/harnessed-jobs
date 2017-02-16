#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys

for i in range(20):
     print "This POWER ON test may be skipped if the REB(s) are(is) already fully powered and you have the authorization. Skip the step (N/y)?"
sys.stdout.flush()
answer = raw_input("\n\nThis test may be skipped if the REB(s) are(is) already fully powered and you have the authorization. Skip the step (N/y)? \n\n")
if "y" in answer.lower() :
     print "Operator requested to skip the step. BYE"
else :
    ccsProducer('ready_acq', 'ccseorebalive_power.py')

for i in range(20):
     print "This EXPOSURES test may be skipped if you have the authorization. Skip the step (N/y)?"
sys.stdout.flush()
answer = raw_input("\n\nThis test may be skipped if you have the authorization. Skip the step (N/y)? \n\n")
if "y" in answer.lower() :
     print "Operator requested to skip the step. BYE"
else :
    ccsProducer('ready_acq', 'ccseorebalive_exposure.py')
    sys.stdout.flush()


apptxt = "Please check the FLAT image that is about to be projected in ds9\nfor correct bias regions.\nClick on this window when ready."

print apptxt
topq = Tkinter.Tk()
q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
q.pack()
topq.title('FLAT image check')
topq.mainloop()

qefiles = sorted(glob.glob('*flat*.fits'))
#for qefile in qefiles:
#os.system("ds9 -scale datasec no -scale histequ %s" % qefile)
if len(qefiles)>0 :
     os.system("ds9 -scale datasec no -scale histequ *flat*fits")

apptxt = "Please check the Fe55 image that is about to be projected in ds9\nfor clearly identifiable X-ray hits that should appear as clusters of pixels.\nClick on this window when ready."

print apptxt
topf = Tkinter.Tk()
f = Tkinter.Button(topf, text = apptxt, command = topf.destroy, bg = "yellow", font = ("Helvetica",24))
f.pack()
topf.title('FE55 image check')
topf.mainloop()

fe55files = sorted(glob.glob('*fe55*.fits'))
#for fe55file in fe55files:
#    os.system("ds9 -mosaicimage iraf -lock frame image -zscale -scale datasec yes %s" % fe55file)
if len(fe55files)>0 :
     os.system("ds9 -mosaicimage iraf -lock frame image -zscale -scale datasec yes *fe55*")

apptxt = "The job is finished.\nClick on this button then\nreturn to the eTraveler page to complete the readiness verification form."
topd = Tkinter.Tk()
d = Tkinter.Button(topd, text = apptxt, command = topd.destroy, bg = "yellow", font = ("Helvetica",24))
d.pack()
topd.title('DONE')
topd.mainloop()
