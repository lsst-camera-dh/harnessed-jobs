#!/usr/bin/env python
import glob
import lcatr.schema
import os
import subprocess
    
results = []


last_data = subprocess.check_output("ssh tsreb@130.199.47.42 ls -rtd /data/* | tail -1", shell=True)
os.system("scp -vp tsreb@130.199.47.42 %s/\* ." % last_data)


os.system("chmod 644 *.*")


files = glob.glob('*.pdf')
files = files + glob.glob('*.txt')

data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

digital_current_check='none'
analog_current_check='none'
clock_current_check='none'
OD_current_check='none'
heater_current_check='none'
slice_check='none'
checker_board_check='none'

results.append(lcatr.schema.valid(lcatr.schema.get('tsreb_upload'),
                            digital_current_check=digital_current_check,
                            analog_current_check=analog_current_check,
                            clock_current_check=clock_current_check,
                            OD_current_check=OD_current_check,
                            heater_current_check=heater_current_check,
                            slice_check=slice_check,
                            checker_board_check=checker_board_check))

results.extend(siteUtils.jobInfo())



lcatr.schema.write_file(results)
lcatr.schema.validate_file()
