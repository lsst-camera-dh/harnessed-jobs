import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob

def getSensorGains(sensor_id, jobname='fe55_analysis'):
    gain_file = dependency_glob('%s_eotest_results.fits' % sensor_id,
                                jobname=jobname)[0]
    data = sensorTest.EOTestResults(gain_file)
    amps = data['AMP']
    gains = data['GAIN']
    sensorGains = dict([(amp, gains[amp-1]) for amp in amps])
    return sensorGains
