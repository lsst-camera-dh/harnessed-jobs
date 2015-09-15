#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils

sensor_id = siteUtils.getUnitId()
sflat_files = siteUtils.dependency_glob('*_sflat_*500*.fits',
                                        jobname=siteUtils.getProcessName('sflat_acq'),
                                        description='Superflat files:')

task = sensorTest.CteTask()
task.run(sensor_id, sflat_files)
