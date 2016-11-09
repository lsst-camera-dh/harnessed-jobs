#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os


ccsProducer('ready_acq', 'ccseorebalive_power.py')
ccsProducer('ready_acq', 'ccseorebalive_exposure.py')
ccsProducer('ready_acq', 'ccseorebalive_power_down.py')

apptxt = "Please check the FLAT image that is about to be projected in ds9\nfor correct bias regions.\nClick on this window when ready."

print apptxt
topq = Tkinter.Tk()
q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
q.pack()
topq.title('FLAT image check')
topq.mainloop()

qefiles = sorted(glob.glob('*flat*.fits'))
for qefile in qefiles:
    os.system("ds9 -scale datasec no -scale histequ %s" % qefile)

apptxt = "Please check the Fe55 image that is about to be projected in ds9\nfor clearly identifiable X-ray hits that should appear as clusters of pixels.\nClick on this window when ready."

print apptxt
topf = Tkinter.Tk()
f = Tkinter.Button(topf, text = apptxt, command = topf.destroy, bg = "yellow", font = ("Helvetica",24))
f.pack()
topf.title('FE55 image check')
topf.mainloop()

fe55files = sorted(glob.glob('*fe55*.fits'))
for fe55file in fe55files:
    os.system("ds9 -scale datasec yes -scale histequ -mosaicimage iraf %s" % fe55file)

apptxt = "The job is finished.\nClick on this button then\nreturn to the eTraveler page to complete the readiness verification form."
topd = Tkinter.Tk()
d = Tkinter.Button(topd, text = apptxt, command = topd.destroy, bg = "yellow", font = ("Helvetica",24))
d.pack()
topd.title('DONE')
topd.mainloop()
