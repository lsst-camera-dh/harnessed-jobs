#!/usr/bin/env python
import glob
import lsst.eotest.sensor as sensorTest
import lcatr.schema
import siteUtils

sensor_id = siteUtils.getUnitId()

results = []

read_noise_file = '%s_eotest_results.fits' % sensor_id
data = sensorTest.EOTestResults(read_noise_file)
amps = data['AMP']
read_noise_data = data['READ_NOISE']
for amp, read_noise in zip(amps, read_noise_data):
    results.append(lcatr.schema.valid(lcatr.schema.get('Read_Noise'),
                                      amp=amp, read_noise=read_noise))

files = glob.glob('*read_noise?*.fits')
files.append(read_noise_file)
data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
