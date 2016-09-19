#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

siteUtils.aggregate_job_ids()
sensor_id = siteUtils.getUnitId()
sflat_files = siteUtils.dependency_glob('*_sflat_500_flat_H*.fits',
                                        jobname=siteUtils.getProcessName('sflat_acq'),
                                        description='Superflat files:')
mask_files = eotestUtils.glob_mask_files()

task = sensorTest.DarkPixelsTask()
task.run(sensor_id, sflat_files, mask_files)
