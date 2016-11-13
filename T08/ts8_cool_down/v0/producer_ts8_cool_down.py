#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os

apptxt = "Warning, this script will turn on the Polycold\nand ramp the temperature to the operating setpoint.\nClick on this button only if this OK. If this is not OK, type abort in any terminal window or click on the abort button on the GUI."

print apptxt
top = Tkinter.Tk()
A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "yellow", font = ("Helvetica",24))
A.pack()
top.title('Ready for cooling?')
top.mainloop()

ccsProducer('ts8_cool_down', 'ccseots8_cool_down.py')
