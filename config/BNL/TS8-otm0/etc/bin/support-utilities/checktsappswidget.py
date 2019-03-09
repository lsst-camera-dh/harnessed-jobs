#!/usr/bin/env python
import os
import sys
import commands
import time
import subprocess
import Tkinter
import tkMessageBox

top = Tkinter.Tk()

false = 1==0
true = 1==1

foundjython = false
foundtrendp = false
foundtrends = false
foundts     = false
foundarchon = false


def updatestat():
    global foundjython
    global foundtrendp
    global foundtrends
    global foundts
    global foundts8
    global A
    global B
    global C
    global D
    global E
    global F

    foundjython = false
    foundtrendp = false
    foundtrends = false
    foundts     = false
    foundts8 = false
    
    pstr = commands.getstatusoutput('ps -fe')

    thispart = "partition=TS8"
    
    for s in pstr :
        if type(s) is str :
            app = "JythonConsole"
            apptxtA = "JythonConsole"
            def stopjy(apptxtA):
                os.system("pkill -f '\-\-app JythonConsole'")
                A.configure(text = "Killing %s" % apptxtA, bg = "red")
            if app in s and thispart in s :
                foundjython = true
                A = Tkinter.Button(top, text ="%s is running" % app, command = lambda : stopjy(apptxtA), bg = "green")
#                print "%s is already running" % app
            app = "TrendingIngestModule"
            if app in s and thispart in s :
                foundtrendp = true
                B = Tkinter.Button(top, text ="%s is running" % app, bg = "green")
#                print "%s is already running" % app
            app = "LocalRestServices"
            if app in s and thispart in s :
                foundtrends = true
                C = Tkinter.Button(top, text ="%s is running" % app, bg = "green")
#                print "%s is already running" % app
            app = "-app ts"
            apptxtD = "Teststand subsystem"
            def stopts(apptxtD):
                os.system("pkill -f '\-app ts'")
                D.configure(text = "Killing %s" % apptxtD, bg = "red")
            if app in s and thispart in s :
                foundts = true
                D = Tkinter.Button(top, text ="%s is running" % app, command = lambda : stopts(apptxtD), bg = "green")
#                print "%s is already running" % app
            app = "-app RunTS8Subsystem"
            apptxtE = "Ts8 subsystem"
            def stopts8(apptxtE):
                os.system("pkill -f '\-app RunTS8Subsystem'")
                E.configure(text = "Killing %s" % apptxtE, bg = "red")
            if app in s and thispart in s :
                foundts8 = true
                E = Tkinter.Button(top, text ="%s is running" % app, command = lambda : stopts8(apptxtE), bg = "green")
#                print "%s is already running" % app

#            print "-----------------------"
            apptxtA = "Jython Console"

            def startjy(apptxtA):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--title=JythonConsole","--command=screen -S jython ./JythonConsole"]);
#    tkMessageBox.showinfo( "Started Jython Console", "Started Jython Console")
                A.configure(text = "Started %s" % apptxtA, bg = "blue")

            if not foundjython :
#                print "Need to start %s" % apptxtA;
                A = Tkinter.Button(top, text ="Start %s" % apptxtA, command = lambda : startjy(apptxtA), bg = "grey")



            apptxtB = "Trending Persister"
            def starttrendp(apptxtB):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--command=./settitle ./trendingPersister"]);
                B.configure(text = "Started %s" % apptxtB, bg = "blue")

            if not foundtrendp :
#                print "Need to start %s" % apptxtB;
                B = Tkinter.Button(top, text ="Start %s" % apptxtB, command = lambda : starttrendp(apptxtB), bg = "grey")



            apptxtC = "Trending Server"
            def starttrends(apptxtC):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--command=./settitle ./trendingServer"]);
                C.configure(text = "Started %s" % apptxtC, bg = "blue")

            if not foundtrends :
#                print "Need to start %s" % apptxtC;
                C = Tkinter.Button(top, text ="Start %s" % apptxtC, command = lambda : starttrends(apptxtC), bg = "grey")



            apptxtD = "TestStand SubSystem"
            def startts(apptxtD):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--title=ts","--command=screen -S ts ./ts"]);
                D.configure(text = "Started %s" % apptxtD, bg = "blue")

            if not foundts :
#                print "Need to start %s" % apptxtD;
                D = Tkinter.Button(top, text ="Start %s" % apptxtD, command = lambda : startts(apptxtD), bg = "grey")

            apptxtE = "Ts8 subsystem"
            def startts8(apptxtE):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--title=ts8","--command=screen -S ts8 ./RunTS8Subsystem"]);
                E.configure(text = "Started %s" % apptxtE, bg = "blue")

            if not foundts8 :
#                print "Need to start %s" % apptxtE;
                E = Tkinter.Button(top, text ="Start %s" % apptxtE, command = lambda : startts8(apptxtE), bg = "grey")
            apptxtF = "CCS Gui"
            def startgui(apptxtF):
                subprocess.Popen(["gnome-terminal","--zoom=0.5","--command=./settitle ./CCS-Console"]);
                F.configure(text = "Started %s" % apptxtF, bg = "blue")

            F = Tkinter.Button(top, text ="Start a %s" % apptxtF, command = lambda : startgui(apptxtF), bg = "grey")

            A.pack()
            B.pack()
            C.pack()
            D.pack()
            E.pack()
            F.pack()

if (foundjython and foundtrendp and foundtrends and foundts and foundts8) :
    print "All required CCS apps found to be running. You are read to go!"

updatestat()

def cleanupdate(A,B,C,D,E,F):
    A.destroy()
    B.destroy()
    C.destroy()
    D.destroy()
    E.destroy()
    F.destroy()
    updatestat()

G = Tkinter.Button(top, text ="Update Status",command= lambda : cleanupdate(A,B,C,D,E,F))

def callclean():
    cleanupdate(A,B,C,D,E,F)
#    time.sleep(2)
    top.after(10000, callclean)

G.pack()
top.title('CCS Apps')
top.after_idle(callclean)
top.mainloop()
