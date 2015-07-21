#!/usr/bin/env python
import lcatr.schema
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
xtalk_file = '%s_xtalk_matrix.fits' % sensor_id

results = [lcatr.schema.fileref.make(xtalk_file),
           siteUtils.packageVersions(),
           eotestUtils.eotestCalibrations()]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
