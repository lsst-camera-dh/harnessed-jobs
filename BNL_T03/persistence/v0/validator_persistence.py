#!/usr/bin/env python
import glob
import pyfits
import numpy as np
import lsst.eotest.image_utils as imutils
import lsst.eotest.sensor as sensorTest
import lcatr.schema
import siteUtils

sensor_id = siteUtils.getUnitId()

# Save the output file from producer script.
persistence_file = '%(sensor_id)s_persistence.fits' % locals()
results = [lcatr.schema.fileref.make(persistence_file)]

# Save the deferred charge for each amplifier from the first post-flat
# dark frame as the image persistence metric.
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
    results.append(lcatr.schema.valid(lcatr.schema.get('persistence'),
                                      amp=amp, median_flux=median_flux,
                                      stdev=stdev))

results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
