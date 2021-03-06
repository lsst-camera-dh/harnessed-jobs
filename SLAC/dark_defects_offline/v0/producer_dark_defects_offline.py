#!/usr/bin/env python
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
sflat_files = siteUtils.datacatalog_glob('*_sflat_500_flat_H*.fits',
                                         testtype='SFLAT_500',
                                         imgtype='FLAT',
                                         description='Superflat files:')
mask_files = eotestUtils.glob_mask_files()

task = sensorTest.DarkPixelsTask()
task.run(sensor_id, sflat_files, mask_files)
