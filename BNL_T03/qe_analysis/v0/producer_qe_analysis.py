#!/usr/bin/env python
import os
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

# The photodiode calibration file for BNL data.
pd_cal_file = os.path.join(os.environ['EOTEST_DIR'], 'data', 'qe',
                           'BNL', 'pd_Cal_mar2013.txt')

lambda_files = dependency_glob('*_lambda_*.fits',
                               jobname=siteUtils.getProcessName('qe_acq'))
mask_files = dependency_glob('*_mask.fits')

print lambda_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.QeTask()
task.run(sensor_id, lambda_files, None, None, None, mask_files, gains,
         pd_cal_file=pd_cal_file)
