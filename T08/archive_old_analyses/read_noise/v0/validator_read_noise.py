#!/usr/bin/env python
import glob
import lsst.eotest.sensor as sensorTest
import lcatr.schema
import siteUtils
import eotestUtils


ccdnames = {}
ccdmanunames = {}
ccdnames,ccdmanunames = siteUtils.getCCDNames()

for sensor_id in ccdnames :

    results = []

    read_noise_file = '%s_eotest_results.fits' % sensor_id
    data = sensorTest.EOTestResults(read_noise_file)
    amps = data['AMP']
    read_noise_data = data['READ_NOISE']
    system_noise_data = data['SYSTEM_NOISE']
    total_noise_data = data['TOTAL_NOISE']
    for amp, read_noise, system_noise, total_noise in zip(amps, read_noise_data,
                                                          system_noise_data,
                                                          total_noise_data):
        print "sensor = %s amp = %d read_noise = %f" % (sensor_id,amp,read_noise)
#        results.append(lcatr.schema.valid(lcatr.schema.get('read_noise'),
#                                          amp=amp, read_noise=read_noise,
#                                          system_noise=system_noise,
#                                          total_noise=total_noise))

        results.extend(siteUtils.jobInfo())

    results.append(eotestUtils.eotestCalibrations())

    fe55_acq_job_id = siteUtils.get_prerequisite_job_id('*/%s_fe55_fe55_*.fits' % sensor_id,
                                                        jobname=siteUtils.getProcessName('fe55_acq'))
    md = dict(system_noise_file=dict(JOB_ID=fe55_acq_job_id))
    results.extend(eotestUtils.eotestCalibsPersist('system_noise_file',
                                                   metadata=md))

    files = glob.glob('*read_noise?*.fits')
    for fitsfile in files:
        eotestUtils.addHeaderData(fitsfile, LSST_NUM=sensor_id, TESTTYPE='FE55',
                              DATE=eotestUtils.utc_now_isoformat(),
                              CCD_MANU=siteUtils.getCcdVendor().upper())


data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
