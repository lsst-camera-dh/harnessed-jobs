#!/usr/bin/env python
import os
import sys
import subprocess
import Tkinter
import tkMessageBox
import time

def syscmnd(cmd) :
    os.system("ssh LSSTuser@172.17.100.2 \"%s\"" % cmd)

def makedirs(idir) :
    syscmnd("mkdir -p %s" % idir)                  


#ogpscriptname = "CCDa_Edge_scan_Abs_hgt_Flatness_robust.RTN"
#ogpscriptname1 = "e2V\_Flat_AbsHgt.RTN"
#ogpscriptname2 = "e2V\_EdgeScan.RTN"
ogpscriptname1 = ""
ogpscriptname2 = ""

versionsFile = open("RTN_versions.txt")
for line in versionsFile:
#    print "line = %s" % line
    values = line.split("|")
    if "e2V_Flat_AbsHgt" in values[0] :
        ogpscriptname1 = values[0]
        print "For Absolute Height, using - %s" % line
    if "e2V_EdgeScan" in values[0] :
        ogpscriptname2 = values[0]
        print "For Edge Scan, using       - %s" % line


ccd = os.environ["LCATR_UNIT_ID"]

topccddir = "/cygdrive/c/Production_DATA/%s" % ccd
print "Creating the top level directory for the CCD at %s" % topccddir

edgedir = "%s/EdgeScan/" % topccddir
print "Creating directory for edge scan results. Location is %s" % edgedir

flatdir = "%s/Metrology/" % topccddir
print "Creating directory for flatness results. Location is %s" % flatdir

tm = time.strftime("%Y%m%d-%HH%MM")

edgedatedir = "%s%s" % (edgedir,tm)
print "Creating dated edge directory for the CCD at %s" % edgedatedir
makedirs(edgedatedir)
syscmnd("chmod 777 %s" %  edgedatedir)
flatdatedir = "%s%s" % (flatdir,tm)
print "Creating dated edge directory for the CCD at %s" % flatdatedir
makedirs(flatdatedir)
syscmnd("chmod 777 %s" %  flatdatedir)
print "Please setup the OGP MeasureMind application to store results in respective edge scan and flatness directories indicated above"

# leave a link to the location where the files should go
cwd = os.getcwd() 
print "Making links to the data directories in %s" % cwd
os.system("ln -s /home/LSSTuser/OGP_mirror%s edgelink" % (edgedatedir));
os.system("ln -s /home/LSSTuser/OGP_mirror%s flatlink" % (flatdatedir));
os.system("ls -lrt" )

#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please setup the OGP MeasureMind application to store<br>edge scan results in %s edgedatedir<br>and<br>flatness results in %s" % (edgedatedir,flatdatedir), bg = "green")
#M=Tkinter.Button(top,text="test")
#M.pack()
#top.title('OGP Dirs Ready')
#top.mainloop()

print "Please setup the OGP MeasureMind application to store\nedge scan results in %s \nand\nflatness results in %s" % (edgedatedir,flatdatedir)
print "============================================="
print "Now installing scripts"
tag = os.environ["OGP_SCRIPTS_TAG"]
ogpscriptshome = os.environ["OGP_SCRIPTS_HOME"]


print "The release of OGP-scripts with tag %s will be installed" % tag
print "copying old installation of OGP scripts to a safe place"
syscmnd("cd %s ; cp -Lrvp OGP-scripts old-OGP-scripts-`date +%%F-%%R`" % ogpscriptshome)
print "moving the original to /tmp"
syscmnd("cd %s ; cp -Lvrp OGP-scripts /tmp/ ; mv OGP-scripts moved-OGP-scripts" % ogpscriptshome)
print "downloading tar of new tag"
syscmnd("cd %s ; wget https://github.com/lsst-camera-dh/OGP-scripts/archive/%s.tar.gz" % (ogpscriptshome,tag))
print "untarring"
syscmnd("cd %s ; tar -vzxf %s.tar.gz" % (ogpscriptshome,tag))
print "making a link to it"
syscmnd("cd %s ; ln -s OGP-scripts-%s OGP-scripts" % (ogpscriptshome,tag))

syscmnd("cp -vp %s/OGP-scripts/Production\ routines/%s %s" % (ogpscriptshome,ogpscriptname1,flatdatedir))
syscmnd("cp -vp %s/OGP-scripts/Production\ routines/%s %s" % (ogpscriptshome,ogpscriptname2,edgedatedir))

syscmnd("cd %s" % cwd)

print "The OGP acquisition and analysis scripts have been installed."

# make a button showing the name that should be used for the output filename
#E2V-CCD250-82-5-G42-14041-08-01_DimMet_20150817-16H23M.DAT
#ccd = os.environ["LCATR_UNIT_ID"]
#dateddir = glob.glob("Flatness/*")
#dirdate = dateddir[0].strip("/")
#dirdate = tm
rtnnam = "%s_DimMet_%s.DAT" % (ccd,tm)
#tkMessageBox.showinfo("OGP Routine Data Output Filename", rtnnam)
#subprocess.Popen(["/home/LSSTuser/lsst/showfl.py",rtnnam]);

print "======================================="
print "OGP Routine Data Output Filename: %s" % rtnnam
print "======================================="


#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="%s_DimMet_%s.DAT" % (ccd,dirdate), command=lambda: w.event_generate("<<Copy>>")), bg = "green")
#M=Tkinter.Button(top,text="filename")
#M.pack()
#top.title('OGP Routine Output Filename')
#top.mainloop()
