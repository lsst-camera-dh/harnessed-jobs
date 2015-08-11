#!/usr/bin/env python
import os
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
dark_files = siteUtils.dependency_glob('*_persistence_dark_*.fits',
                                       jobname=siteUtils.getProcessName('persist_acq'),
                                       description='Dark files:')
flat = siteUtils.dependency_glob('*_persistence_flat_*.fits',
                                 jobname=siteUtils.getProcessName('persist_acq'),
                                 description='Flat file:')[0]

pre_flat_darks = dark_files[:3]
post_flat_darks = dark_files[3:]

mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.PersistenceTask()
task.run(sensor_id, pre_flat_darks, flat, post_flat_darks, mask_files, gains)
