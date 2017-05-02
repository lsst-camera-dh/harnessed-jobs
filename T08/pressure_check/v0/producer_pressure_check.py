#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os

apptxt = "Doing pressure check."

#print apptxt
#top = Tkinter.Tk()
#A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "yellow", font = ("Helvetica",24))
#A.pack()
#top.title('Performing pressure check')
#top.mainloop()

ccsProducer('pressure_check', 'ccseopressure_check.py')
