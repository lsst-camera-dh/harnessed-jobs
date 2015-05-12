import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

def getSensorGains(sensor_id, jobname='fe55_analysis'):
    processName = siteUtils.getProcessName(jobname)
    gain_file = dependency_glob('%s_eotest_results.fits' % sensor_id,
                                jobname=processName)[0]
    data = sensorTest.EOTestResults(gain_file)
    amps = data['AMP']
    gains = data['GAIN']
    sensorGains = dict([(amp, gains[amp-1]) for amp in amps])
    return sensorGains
