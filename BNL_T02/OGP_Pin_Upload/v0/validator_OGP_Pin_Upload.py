#!/usr/bin/env python
import glob
import lcatr.schema
import subprocess
import os
import Tkinter
import tkMessageBox

#import siteUtils

results = []
ogpdir = subprocess.check_output("ls -rtd %s/../../../../*/Make-OGP-Pin-Directories/v0/* | tail -1" % os.getcwd(), shell=True)


theogppindir = os.path.realpath("%s/pinlink/" % ogpdir.strip("\n"))

os.mkdir("LateralPosition")

os.system("cp -r /%s LateralPosition/" % theogppindir.strip("/"))

print "looking for link to absolute height files in %s" % (theogppindir)

os.system("chmod 644 LateralPosition/*/*.*")
pinfiles = glob.glob("LateralPosition/*/*.*")

os.system("rm -rf /cygdrive/c/DATA/Image\ files\ old")
os.system("mv /cygdrive/c/DATA/Image\ files /cygdrive/c/DATA/Image\ files\ old")
os.system("mkdir /cygdrive/c/DATA/Image\ files")

data_products1 = [lcatr.schema.fileref.make(item) for item in pinfiles]
results.extend(data_products1)


for item in pinfiles :
    print "Archiving LateralPosition file - %s" % item


lcatr.schema.write_file(results)
lcatr.schema.validate_file()

# make a button showing the name that should be used for the output filename
#E2V-CCD250-82-5-G42-14041-08-01_DimMet_20150817-16H23M.DAT
#ccd = os.environ["LCATR_UNIT_ID"]
#dateddir = glob.glob("LateralPosition/*")
#dirdate = dateddir[0].strip("/")
#tkMessageBox.showinfo("OGP Routine Output Filename", "%s_Pin_%s.DAT" % (ccd,dirdate))
#top = Tkinter.Tk()
#M = Tkinter.Button(top, text ="Please use the following filename as the specification of the output filename\n%s_Pin_%s.DAT" % (ccd,dirdate), bg = "green")
#M=Tkinter.Button(top,text="filename")
#M.pack()
#top.title('OGP Routine Output Filename')
#top.mainloop()
