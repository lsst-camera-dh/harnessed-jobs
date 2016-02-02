#!/usr/bin/env python
import glob
import pyfits
import numpy as np
import lsst.eotest.image_utils as imutils
import lsst.eotest.sensor as sensorTest
import lcatr.schema
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()

# Save the output file from producer script.
persistence_file = '%(sensor_id)s_persistence.fits' % locals()
eotestUtils.addHeaderData(persistence_file, LSST_NUM=sensor_id,
                          TESTTYPE='PERSISTENCE',
                          DATE=eotestUtils.utc_now_isoformat(),
                          CCD_MANU=siteUtils.getCcdVendor().upper())

results = [lcatr.schema.fileref.make(persistence_file)]

# Save the deferred charge for each amplifier from the first post-flat
# dark frame as the image persistence metric.
#
# Read the results from the FITS file.
persistence = pyfits.open(persistence_file)
times = persistence[1].data.field('TIME')

# Times of dark frames are relative to the MJD-OBS of the flat.
post_flat_times = times[np.where(times > 0)]
index = np.where(times == min(post_flat_times))[0][0]

# Loop over amplifiers and record the deferred charge (median pixel
# value and stdev) in the first post-flat dark frame.
for amp in imutils.allAmps:
    median_flux = persistence[1].data.field('MEDIAN%02i' % amp)[index]
    stdev = persistence[1].data.field('STDEV%02i' % amp)[index]
    results.append(lcatr.schema.valid(lcatr.schema.get('persistence'), amp=amp,
                                      deferred_charge_median=median_flux,
                                      deferred_charge_stdev=stdev))

results.extend(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
