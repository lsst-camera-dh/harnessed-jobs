#!/usr/bin/env python
import os
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

siteUtils.aggregate_job_ids()
sensor_id = siteUtils.getUnitId()
lambda_files = siteUtils.dependency_glob('*_lambda_flat_*.fits',
                                         jobname=siteUtils.getProcessName('qe_acq'),
                                         description='Lambda files:')

pd_ratio_file = eotestUtils.getPhotodiodeRatioFile()
if pd_ratio_file is None:
    message = ("The test-stand specific photodiode ratio file is " +
               "not given in config/%s/eotest_calibrations.cfg."
               % siteUtils.getSiteName())
    raise RuntimeError(message)

correction_image = eotestUtils.getIlluminationNonUniformityImage()
if correction_image is None:
    print
    print "WARNING: The correction image file is not given in"
    print "config/%s/eotest_calibrations.cfg." % siteUtils.getSiteName()
    print "No correction for non-uniform illumination will be applied."
    print
    sys.stdout.flush()

mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.QeTask()
task.run(sensor_id, lambda_files, pd_ratio_file, mask_files, gains,
         correction_image=correction_image)
