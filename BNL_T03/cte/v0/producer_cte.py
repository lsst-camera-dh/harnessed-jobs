#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()

gains = eotestUtils.getSensorGains(jobname='fe55_analysis')
sflat_high_files = siteUtils.dependency_glob('*_sflat_500_flat_H*.fits',
                                             jobname=siteUtils.getProcessName('sflat_acq'),
                                             description='Superflat high flux files:')

task = sensorTest.CteTask()
task.run(sensor_id, sflat_high_files, flux_level='high', gains=gains)

sflat_low_files = siteUtils.dependency_glob('*_sflat_500_flat_L*.fits',
                                            jobname=siteUtils.getProcessName('sflat_acq'),
                                            description='Superflat low flux files:')
task.run(sensor_id, sflat_low_files, flux_level='low', gains=gains)
