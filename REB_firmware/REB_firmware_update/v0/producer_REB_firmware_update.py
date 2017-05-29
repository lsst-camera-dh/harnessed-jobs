#!/usr/bin/env python
import glob
import os
import subprocess

#Copy firmware_load_scripts files
instdir = os.getenv('LCATR_INSTALL_AREA').replace('share/','')
os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/et_prog_flash.sh .', instdir)
os.system('cp -vp %s/REB_v5/firmware_load_scripts/bin/flash_load.tcl .', instdir)

#Get list of files in firmware directory
list_of_firmware_files = glob.glob(os.path.join(instdir,'/REB_v5/targets/REB_v5_top/images/', '*.mcs'))

#Find most recent file
recent_file = max(list_of_firmware_files, key=os.path.getctime)
    
#Call Stefano's REB5 firmware upgrade program
subprocess.check_call(['source et_prog_flash.sh ', '/REB_v5/targets/REB_v5_top/images/' + recent_file])
