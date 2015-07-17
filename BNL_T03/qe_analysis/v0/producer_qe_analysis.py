#!/usr/bin/env python
import os
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
lambda_files = siteUtils.dependency_glob('*_lambda_*.fits',
                                         jobname=siteUtils.getProcessName('qe_acq'),
                                         description='Lambda files:')

pd_ratio_file = eotestUtils.getPhotodiodeRatioFile()
if pd_ratio_file is None:
    pd_ratio_file = os.path.join(os.environ['EOTEST_DIR'], 'data', 'qe',
                                 'BNL', 'pd_Cal_mar2013_v1.txt')
    print 
    print "WARNING: The test-stand specific photodiode ratio file is"
    print "not given in config/%s/eotest_calibrations.cfg." % siteUtils.getSiteName()
    print "Using instead", pd_ratio_file
    print
    sys.stdout.flush()

mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.QeTask()
task.run(sensor_id, lambda_files, pd_ratio_file, mask_files, gains)
