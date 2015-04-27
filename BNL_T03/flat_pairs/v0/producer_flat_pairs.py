#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils
import eotestUtils

flat_files = dependency_glob('*_flat*flat?_*.fits', jobname='flat_acq')
mask_files = dependency_glob('*_mask.fits')
print flat_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(sensor_id)

task = sensorTest.FlatPairTask()
task.run(sensor_id, flat_files, mask_files, gains)
