#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

trap_file = dependency_glob('*_trap_ppump*.fits', jobname='ppump_acq')[0]
mask_files = dependency_glob('*_mask.fits')

print trap_file
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.TrapTask()
task.run(sensor_id, trap_file, mask_files, gains)
