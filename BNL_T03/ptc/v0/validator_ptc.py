#!/usr/bin/env python
import lcatr.schema
import siteUtils

sensor_id = siteUtils.getUnitId()
ptc_results = '%s_ptc.fits' % sensor_id

results = [lcatr.schema.fileref.make(ptc_results)]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
