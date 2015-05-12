#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

dark_files = dependency_glob('*_dark_dark_*.fits',
                             jobname=siteUtils.getProcessName('dark_acq'))
mask_files = dependency_glob('*_mask.fits')

print dark_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.DarkCurrentTask()
task.run(sensor_id, dark_files, mask_files, gains)
