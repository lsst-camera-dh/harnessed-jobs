#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter

apptxt = "Warning, this script will turn on the Polycold\nand ramp the temperature to the operating setpoint.\nClick on this button only if this OK."

print apptxt
top = Tkinter.Tk()
A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "pink")
A.pack()
top.title('Ready for cooling?')
top.mainloop()

ccsProducer('ready_acq', 'ccseoready.py')
