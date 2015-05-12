#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

superflat_files = dependency_glob('*_superflat*.fits',
                                  jobname=siteUtils.getProcessName('sflat_acq'))
mask_files = dependency_glob('*_mask.fits')

print superflat_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

task = sensorTest.CteTask()
task.run(sensor_id, superflat_files, mask_files)
