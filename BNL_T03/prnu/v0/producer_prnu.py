#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

lambda_files = dependency_glob('*_lambda_*.fits', jobname='qe_acq')
correction_image = None
mask_files = dependency_glob('*_mask.fits')

print lambda_files
print correction_image
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.PrnuTask()
task.run(sensor_id, lambda_files, mask_files, gains, correction_image)
