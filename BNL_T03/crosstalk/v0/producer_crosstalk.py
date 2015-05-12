#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

spot_files = dependency_glob('*_spot_*.fits',
                             jobname=siteUtils.getProcessName('xtalk_acq'))
mask_files = dependency_glob('*_mask.fits')
print spot_files
print mask_files
sys.stdout.flush()

sensor_id = siteUtils.getUnitId()

task = sensorTest.CrosstalkTask()
task.run(sensor_id, spot_files, mask_files)
