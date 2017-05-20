#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import subprocess

instdir = os.getenv('LCATR_INSTALL_AREA').replace('share/','')

os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/et_prog_flash.sh .')
os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/flash_load.tcl .')
os.system('cp -vp %s/REB_v5/targets/REB_v5_top/images/REB_v5_top_30325002.mcs .')

apptxt = "Click on this window when ready to start firmware update of the first REB"

for i in range(10): 
    print apptxt
    top = Tkinter.Tk()
    A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "yellow", font = ("Helvetica",24))
    A.pack()
    top.title('Ready to start firmware update?')
    top.mainloop()

    os.system('source et_prog_flash.sh REB_v5_top_30325002.mcs')


    print "Rebooting the RCE after a 5s wait"
    time.sleep(5.0)
    sout = subprocess.check_output("$HOME/rebootrce.sh", shell=True)
    print sout
    time.sleep(3.0)
    
    print "Update another REB (Y/N)?"
    sys.stdout.flush()
    answer = raw_input("\n\nUpdate another REB (Y/N)?")
    if not "y" in answer.lower() :
        break


