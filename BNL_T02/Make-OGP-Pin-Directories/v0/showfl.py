#!/usr/bin/env python
import os
import sys
import commands
import subprocess
import Tkinter
import tkMessageBox

top = Tkinter.Tk()

global A

msg = args[1]

def toclipboard(themsg):
    os.system("cat > /dev/clipboard %s" % themsg)
    A.configure(text = "Copied %s to the clipboard" % themsg, bg = "green")

A = Tkinter.Button(top, text ="click to copy %s to clipboard" % msg, command = lambda : toclipboard(msg), bg = "grey")

A.pack()
top.title('OGP output data filename')
#top.after_idle(callclean)
top.mainloop()
