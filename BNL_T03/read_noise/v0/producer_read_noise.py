#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

bias_files = dependency_glob('*_fe55_bias_*.fits', jobname='fe55_acq')
system_noise_files = dependency_glob('noise_*.fits', jobname='system_noise')
mask_files = dependency_glob('*_mask.fits')

if not system_noise_files:
    system_noise_files = None

print bias_files
print system_noise_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()
gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.ReadNoiseTask()
task.run(sensor_id, bias_files, gains,
         system_noise_files=system_noise_files, mask_files=mask_files)
