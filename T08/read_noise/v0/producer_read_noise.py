#!/usr/bin/env python
import sys
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils
import os

siteUtils.aggregate_job_ids()

ccdnames = {}
ccdmanunames = {}
ccdnames,ccdmanunames = siteUtils.getCCDNames()

for sensor_id in ccdnames :

#
# Use Fe55 exposures and the overscan region instead of the bias frames
# as per 2015-09-10 TS1-TS3 sprint decision:
# https://confluence.slac.stanford.edu/display/LSSTCAM/Science+Raft+Teststands
#
    biasgz_files = siteUtils.dependency_glob('*/%s_fe55_fe55_*.fits.gz' % sensor_id,
                                           jobname=siteUtils.getProcessName('fe55_acq'),
                                           description='Fe55 files for read noise:')
    for biasgz_file in biasgz_files :
        os.system("gunzip -v %s" % biasgz_file)
    bias_files = siteUtils.dependency_glob('*/%s_fe55_fe55_*.fits' % sensor_id,
                                           jobname=siteUtils.getProcessName('fe55_acq'),
                                           description='Fe55 files for read noise:')
    gains = eotestUtils.getSensorGains()
    system_noise = eotestUtils.getSystemNoise(gains)
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
             mask_files=mask_files, use_overscan=True)
