#!/usr/bin/env python
from ccsTools import ccsProducer
from java.lang import Exception
import Tkinter
import glob
import os
import subprocess

CCS.setThrowExceptions(True);

#Copy firmware_load_scripts files
instdir = os.getenv('LCATR_INSTALL_AREA').replace('share/','')
os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/et_prog_flash.sh .', instdir)
os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/flash_load.tcl .', instdir)

#Safety button
apptxt = "Click here when ready to start firmware update of the REB"
print apptxt
top = Tkinter.Tk()
A = Tkinter.Button(top, text = apptxt, command = top.destroy, bg = "yellow", font = ("Helvetica",24))
A.pack()
top.title('Are you ready to start the firmware update?')
top.mainloop()

#Get list of files in firmware directory
list_of_firmware_files = glob.glob(os.path.join(instdir,'/REB_v5/targets/REB_v5_top/images/', '*.mcs'))

#Find most recent file
recent_file = max(list_of_firmware_files, key=os.path.getctime)
    
#Call Stefano's REB5 firmware upgrade program
try:
    subprocess.call(['source et_prog_flash.sh ', '/path/to/directory/' + recent_file])
except:
    print "Failed to launch firmware update program. Is vivado installed?"

#Stefano's software should reboot RCE automaticaly
#print "Rebooting the RCE after a 5s wait"
#time.sleep(5.0)
#sout = subprocess.check_output("$HOME/rebootrce.sh", shell=True)
#print sout
#time.sleep(3.0)
