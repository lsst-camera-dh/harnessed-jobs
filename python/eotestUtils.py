import os
import shutil
import socket
import datetime
import numpy as np
import ConfigParser
import astropy.io.fits as pyfits
import lsst.eotest.sensor as sensorTest
import lcatr.schema
from lcatr.harness.helpers import dependency_glob
import siteUtils

def utc_now_isoformat():
    return datetime.datetime.utcnow().isoformat()

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
    try:
        pars = siteUtils.Parfile(getEotestCalibsFile(), getTestStandHostName())
    except ConfigParser.NoSectionError:
        # Use the "default" section.
        pars = siteUtils.Parfile(getEotestCalibsFile(), 'default')
    return pars

def getSystemNoise(gains):
    """
    Return the system noise for each amplifier channel.  The data are
    read from the local file given in the site-specific eotest
    calibrations file.
    """
    pars = getEotestCalibs()
    if pars['system_noise_file'] is None:
        return None
    data = np.recfromtxt(pars['system_noise_file'], names=('amp', 'noise'))
    sys_noise = {}
    # Multiply by gain to obtain noise in e- rms.
    for amp, noise in zip(data['amp'], data['noise']):
        sys_noise[amp] = gains[amp]*noise
    return sys_noise

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

def eotestCalibsPersist(*keys):
    """
    Loop through specified list of keys in eotest calibration config
    file and persist as lcatr.schema.filerefs.  Return the list of
    filerefs.
    """
    pars = getEotestCalibs()
    results = []
    for key in keys:
        filename = pars[key]
        if filename is not None:
            if not os.path.isfile(filename):
                raise RuntimeError("eotest calibration parameter %s = %s is not a valid file" % (key, filename))
            shutil.copy(filename, '.')
            results.append(lcatr.schema.fileref.make(os.path.basename(filename)))
    return results

def addHeaderData(fitsfile, **kwds):
    fits_obj = pyfits.open(fitsfile, do_not_scale_image_data=True)
    try:
        hdu = kwds['hdu']
    except KeyError:
        hdu = 0
    for key, value in kwds.items():
        if key == 'clobber':
            continue
        fits_obj[hdu].header[key] = siteUtils.cast(value)
    try:
        clobber = kwds['clobber']
    except KeyError:
        clobber = True
    # Preserve bitpix for all image extensions since astropy.io.fits 
    # always chage
    fits_obj.writeto(fitsfile, clobber=clobber)
