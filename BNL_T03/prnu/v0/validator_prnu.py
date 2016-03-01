#!/usr/bin/env python
import numpy as np
import pyfits
import lcatr.schema
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()

results_file = '%s_eotest_results.fits' % sensor_id
prnu_results = pyfits.open(results_file)['PRNU_RESULTS'].data

results = []
for wl, stdev, mean in zip(prnu_results['WAVELENGTH'],
                           prnu_results['STDEV'], prnu_results['MEAN']):
    results.append(lcatr.schema.valid(lcatr.schema.get('prnu'),
                                      wavelength=int(np.round(wl)),
                                      pixel_stdev=stdev, pixel_mean=mean))
results.append(siteUtils.packageVersions())
results.extend(siteUtils.jobInfo())
results.append(eotestUtils.eotestCalibrations())

qe_acq_job_id = siteUtils.get_prerequisite_job_id('*_lambda_flat_*.fits',
                                                  jobname=siteUtils.getProcessName('qe_acq'))
md = dict(illumination_non_uniformity_file=dict(JOB_ID=qe_acq_job_id))
results.extend(eotestUtils.eotestCalibsPersist('illumination_non_uniformity_file',
                                               metadata=md))

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
