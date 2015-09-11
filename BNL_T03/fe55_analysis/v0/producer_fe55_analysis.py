#!/usr/bin/env python
import os
import lsst.eotest.sensor as sensorTest
import siteUtils

sensor_id = siteUtils.getUnitId()
fe55_files = siteUtils.dependency_glob('*_fe55_fe55_*.fits',
                                       jobname=siteUtils.getProcessName('fe55_acq'),
                                       description='Fe55 files:')

# Roll-off defects mask needs an input file to get the vendor
# geometry, and will be used for all analyses.
rolloff_mask_file = '%s_rolloff_defects_mask.fits' % sensor_id
sensorTest.rolloff_mask(fe55_files[0], rolloff_mask_file)

task = sensorTest.Fe55Task()
task.run(sensor_id, fe55_files, (rolloff_mask_file,), accuracy_req=0.01)
