#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
flat_files = siteUtils.dependency_glob('*_flat*flat?_*.fits',
                                       jobname=siteUtils.getProcessName('flat_acq'),
                                       description='Flat files:')
mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.FlatPairTask()
task.run(sensor_id, flat_files, mask_files, gains)
