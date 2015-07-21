#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
spot_files = siteUtils.dependency_glob('*_spot_*.fits',
                                       jobname=siteUtils.getProcessName('xtalk_acq'),
                                       description='Spot files:')
mask_files = eotestUtils.glob_mask_files()
system_xtalk_file = eotestUtils.getSystemCrosstalkFile()
if system_xtalk_file is None:
    print 
    print "WARNING: The system crosstalk file is not given in"
    print "config/%s/eotest_calibrations.cfg." % siteUtils.getSiteName()
    print "No correction for system crosstalk will be performed."
    print
    sys.stdout.flush()

task = sensorTest.CrosstalkTask()
task.run(sensor_id, spot_files, mask_files, system_xtalk_file=system_xtalk_file)
