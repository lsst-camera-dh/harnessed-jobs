#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
trap_file = siteUtils.dependency_glob('*_trap_ppump_*.fits',
                                      jobname=siteUtils.getProcessName('ppump_acq'),
                                      description='Trap file:')[0]
mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.TrapTask()
task.run(sensor_id, trap_file, mask_files, gains)
