#!/usr/bin/env python
import os
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

# @todo replace all this with locations of PD calibration data.
sensorTestDir = os.path.split(sensorTest.__file__)[0]
ccd_cal_file = os.path.join(sensorTestDir, 'qe', 'OD142.csv')
sph_cal_file = os.path.join(sensorTestDir, 'qe', 'OD143.csv')
wlscan_file = os.path.join(sensorTestDir, 'qe', 'WLscan.txt')

lambda_files = dependency_glob('*_lambda_*.fits',
                               jobname=siteUtils.getProcessName('qe_acq'))
mask_files = dependency_glob('*_mask.fits')

print lambda_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.QeTask()
task.run(sensor_id, lambda_files, ccd_cal_file, sph_cal_file,
         wlscan_file, mask_files, gains)
