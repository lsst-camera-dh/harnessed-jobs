#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
bias_files = siteUtils.dependency_glob('*_fe55_bias_*.fits',
                                       jobname=siteUtils.getProcessName('fe55_acq'),
                                       description='Bias files:')
gains = eotestUtils.getSensorGains()
system_noise = eotestUtils.getSystemNoise()
if system_noise is None:
    print 
    print "WARNING: The system noise file is not given in"
    print "config/%s/eotest_calibrations.cfg." % siteUtils.getSiteName()
    print "The system noise will be set to zero for all amplifiers."
    print
    sys.stdout.flush()

mask_files = eotestUtils.glob_mask_files()

task = sensorTest.ReadNoiseTask()
task.run(sensor_id, bias_files, gains, system_noise=system_noise,
         mask_files=mask_files)
