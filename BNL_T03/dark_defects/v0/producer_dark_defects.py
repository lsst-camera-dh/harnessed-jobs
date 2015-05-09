#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

sflat_files = dependency_glob('*_superflat_500_*.fits', jobname='sflat_acq')
mask_files = dependency_glob('*_mask.fits')

print sflat_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

task = sensorTest.DarkPixelsTask()
task.run(sensor_id, sflat_files, mask_files)
