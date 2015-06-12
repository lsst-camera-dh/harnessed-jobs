#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
spot_files = siteUtils.dependency_glob('*_spot_*.fits',
                                       jobname=siteUtils.getProcessName('xtalk_acq'),
                                       description='Spot files:')
mask_files = eotestUtils.glob_mask_files()

task = sensorTest.CrosstalkTask()
task.run(sensor_id, spot_files, mask_files)
