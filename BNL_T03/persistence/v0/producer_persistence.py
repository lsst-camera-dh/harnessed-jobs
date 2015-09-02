#!/usr/bin/env python
import os
import lsst.eotest.sensor as sensorTest
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
dark_files = siteUtils.dependency_glob('*_persist*_dark_*.fits',
                                       jobname=siteUtils.getProcessName('persist_acq'),
                                       description='Dark files:')

flat = siteUtils.dependency_glob('*_persist*_flat_*.fits',
                                 jobname=siteUtils.getProcessName('persist_acq'),
                                 description='Flat file:')[0]

ipre = 0
ipos = 0
pre_flat_darks = range(3)
post_flat_darks = range(10)

for fl in dark_files:
    if ("dark_000" in fl or "dark_001" in fl or "dark_002" in fl) :
        pre_flat_darks[ipre] = fl
        ipre = ipre + 1
    else :
        post_flat_darks[ipos] = fl
        ipos = ipos + 1

print "pre_flat_dark_files = "
print pre_flat_darks

print "post_flat_dark_files = "
print post_flat_darks

#pre_flat_darks = dark_files[:3]
#post_flat_darks = dark_files[3:]

mask_files = eotestUtils.glob_mask_files()
gains = eotestUtils.getSensorGains()

task = sensorTest.PersistenceTask()
task.run(sensor_id, pre_flat_darks, flat, post_flat_darks, mask_files, gains)
