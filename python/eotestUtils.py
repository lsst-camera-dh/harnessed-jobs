import os
import socket
import numpy as np
import lsst.eotest.sensor as sensorTest
import lcatr.schema
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

def getTestStandHostName():
    """
    It is assumed that the test stand will be identified by the
    hostname of the dedicated computer used to control it.
    """
    if os.environ.has_key('EOTEST_HOST_DEV'):
        # For running  in development mode without a real test stand.
        return os.environ['EOTEST_HOST_DEV']
    return socket.gethostname()

def getEotestCalibsFile():
    """
    Return the full path to the eotest calibrations file.
    """
    return os.path.join(siteUtils.configDir(), 'eotest_calibrations.cfg')

def getEotestCalibs():
    """
    Return calibration file names for the current test stand.  
    """
    pars = siteUtils.Parfile(getEotestCalibsFile(), getTestStandHostName())
    return pars

def getSystemNoise():
    """
    Return the system noise for each amplifier channel.  The data are
    read from the local file given in site-specific eotest
    calibrations file.
    """
    pars = getEotestCalibs()
    if pars['system_noise_file'] is None:
        return None
    data = np.recfromtxt(pars['system_noise_file'], names=('amp', 'noise'))
    return dict([x for x in zip(data['amp'], data['noise'])])

def eotest_abspath(path):
    if path is None:
        return None
    return os.path.abspath(path)

def getSystemCrosstalkFile():
    """
    Return the full path to the system crosstalk file as given in the
    site-specific eotest calibrations file.
    """
    pars = getEotestCalibs()
    return eotest_abspath(pars['system_crosstalk_file'])

def getPhotodiodeRatioFile():
    """
    Return the full path to the locally accessible monitoring
    photodiode "ratio" file image as given in the site-specific eotest
    calibrations file.
    """
    pars = getEotestCalibs()
    return eotest_abspath(pars['photodiode_ratio_file'])

def getIlluminationNonUniformityImage():
    """
    Return the full path to the locally accessible illumination
    non-uniformity image as as given in the site-specific eotest
    calibrations file.
    """
    pars = getEotestCalibs()
    return eotest_abspath(pars['illumination_non_uniformity_file'])

def eotestCalibrations():
    """
    Return the lcatr.schema.valid results object for persisting the
    eotest calibration file information.
    """
    pars = getEotestCalibs()
    kwds = dict([(key, str(value)) for key, value in pars.items()])
    kwds['eotest_host'] = getTestStandHostName()
    result = lcatr.schema.valid(lcatr.schema.get('eotest_calibrations'), **kwds)
    return result
