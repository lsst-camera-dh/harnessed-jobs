#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os


ccsProducer('ready_acq', 'ccseoready.py')

apptxt = "Please check the FLAT image that is about to be projected in ds9\nfor correct bias regions.\nClick on this window when ready."

print apptxt
topq = Tkinter.Tk()
q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
q.pack()
topq.title('FLAT image check')
topq.mainloop()

qefiles = sorted(glob.glob('*lambda*.fits'))
os.system("ds9 -scale datasec no -scale histequ %s" % qefiles[0])

apptxt = "Please check the Fe55 image that is about to be projected in ds9\nfor clearly identifiable X-ray hits that should appear as clusters of pixels.\nClick on this window when ready."

print apptxt
topf = Tkinter.Tk()
f = Tkinter.Button(topf, text = apptxt, command = topf.destroy, bg = "yellow", font = ("Helvetica",24))
f.pack()
topf.title('FE55 image check')
topf.mainloop()

fe55files = sorted(glob.glob('*fe55*.fits'))
os.system("ds9 -scale datasec yes -scale histequ -mosaicimage %s" % fe55files[0])

apptxt = "The job is finished.\nClick on this button then\nreturn to the eTraveler page to complete the readiness verification form."
topd = Tkinter.Tk()
d = Tkinter.Button(topd, text = apptxt, command = topd.destroy, bg = "yellow", font = ("Helvetica",24))
d.pack()
topd.title('DONE')
topd.mainloop()
