#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
lambda_files = siteUtils.dependency_glob('*_lambda_flat_*.fits',
                                         jobname=siteUtils.getProcessName('qe_acq'),
                                         description='Lambda files:')
mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()
correction_image = eotestUtils.getIlluminationNonUniformityImage()
if correction_image is None:
    print 
    print "WARNING: The correction image file is not given in"
    print "config/%s/eotest_calibrations.cfg." % siteUtils.getSiteName()
    print "No correction for non-uniform illumination will be applied."
    print
    sys.stdout.flush()

task = sensorTest.PrnuTask()
task.run(sensor_id, lambda_files, mask_files, gains, correction_image)
