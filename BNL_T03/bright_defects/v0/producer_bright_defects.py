#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

dark_files = dependency_glob('*_dark_dark_*.fits', jobname='dark_acq')
mask_files = dependency_glob('*_mask.fits', jobname='fe55_analysis')

print dark_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.BrightPixelsTask()
task.run(sensor_id, dark_files, mask_files, gains)
