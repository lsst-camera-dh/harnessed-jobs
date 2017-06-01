#!/usr/bin/env python
import glob
import os
import subprocess

#Get install directory path
instdir = os.getenv('REB_V5DIR')

#Change directory to dir containing firmware scripts
os.chdir("%s/firmware_load_scripts/bin/" % instdir)

#Get list of files in firmware directory
fullpath = instdir+'/targets/REB_v5_top/images/'
list_of_firmware_files = glob.glob(fullpath+'*.mcs*')

#Find most recent file
recent_file = max(list_of_firmware_files, key=os.path.getctime)
    
#Call Stefano's REB5 firmware upgrade program
subprocess.check_output(['./et_prog_flash.sh', recent_file])
