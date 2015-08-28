#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os

apptxt = "Warning, this script will turn on the Polycold\nand ramp the temperature to the operating setpoint.\nClick on this button only if this OK."

print apptxt
top = Tkinter.Tk()
A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "yellow", font = ("Helvetica",24))
A.pack()
top.title('Ready for cooling?')
top.mainloop()

ccsProducer('ts3_cool_down_acq', 'ccseots3_cool_down.py')


apptxt = "Please check the FLAT image that is about to be projected in ds9\nfor correct bias regions.\nClick on this window when ts3_cool_down."

print apptxt
topq = Tkinter.Tk()
q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
q.pack()
topq.title('FLAT image check')
topq.mainloop()

qefiles = sorted(glob.glob('*lambda*.fits'))
os.system("ds9 -scale datasec no -scale histequ %s" % qefiles[0])

apptxt = "Please check the Fe55 image that is about to be projected in ds9\nfor clearly identifiable X-ray hits that should appear as clusters of pixels.\nClick on this window when ts3_cool_down."

print apptxt
topf = Tkinter.Tk()
f = Tkinter.Button(topf, text = apptxt, command = topf.destroy, bg = "yellow", font = ("Helvetica",24))
f.pack()
topf.title('FLAT image check')
topf.mainloop()

fe55files = sorted(glob.glob('*fe55*.fits'))
os.system("ds9 -scale datasec no -scale histequ %s" % fe55files[0])

apptxt = "The job is finished. Please click on this window and return to the eTraveler page to complete the form."

print apptxt
topd = Tkinter.Tk()
d = Tkinter.Button(topd, text = apptxt, command = topd.destroy, bg = "yellow", font = ("Helvetica",24))
d.pack()
topd.title('DONE')
topd.mainloop()
