#!/usr/bin/env python
import os
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
lambda_files = siteUtils.dependency_glob('*_lambda_*.fits',
                                         jobname=siteUtils.getProcessName('qe_acq'),
                                         description='Lambda files:')
mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

# The photodiode ratio file for BNL data.
# @todo Replace with ratio file for production work when it is available.
pd_cal_file = os.path.join(os.environ['EOTEST_DIR'], 'data', 'qe',
                           'BNL', 'pd_Cal_mar2013.txt')

task = sensorTest.QeTask()
task.run(sensor_id, lambda_files, None, None, None, mask_files, gains,
         pd_cal_file=pd_cal_file)
