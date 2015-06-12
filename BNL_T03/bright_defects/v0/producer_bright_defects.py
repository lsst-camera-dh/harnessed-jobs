#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
dark_files = siteUtils.dependency_glob('*_dark_dark_*.fits',
                                       jobname=siteUtils.getProcessName('dark_acq'),
                                       description='Dark files:')
mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.BrightPixelsTask()
task.run(sensor_id, dark_files, mask_files, gains)
