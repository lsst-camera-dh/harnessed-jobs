#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils

sensor_id = siteUtils.getUnitId()
sflat_high_files = siteUtils.dependency_glob('*_sflat_*500_flat_H*.fits',
                                             jobname=siteUtils.getProcessName('sflat_acq'),
                                             description='Superflat high flux files:')

task = sensorTest.CteTask()
task.run(sensor_id, sflat_high_files, flux_level='high')

sflat_low_files = siteUtils.dependency_glob('*_sflat_*500_flat_L*.fits',
                                            jobname=siteUtils.getProcessName('sflat_acq'),
                                            description='Superflat low flux files:')
task.run(sensor_id, sflat_low_files, flux_level='low')
