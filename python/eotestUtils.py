import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

def getSensorGains(jobname='fe55_analysis'):
    sensor_id = siteUtils.getUnitId()
    processName = siteUtils.getProcessName(jobname)
    try:
        gain_file = dependency_glob('%s_eotest_results.fits' % sensor_id,
                                    jobname=processName)[0]
    except IndexError:
        raise RuntimeError('eotestUtils.getSensorGains: %s %s' 
                           % (sensor_id, processName))
    data = sensorTest.EOTestResults(gain_file)
    amps = data['AMP']
    gains = data['GAIN']
    sensorGains = dict([(amp, gains[amp-1]) for amp in amps])
    return sensorGains

def glob_mask_files(pattern='*_mask.fits'):
    return siteUtils.dependency_glob(pattern, description='Mask files:')
