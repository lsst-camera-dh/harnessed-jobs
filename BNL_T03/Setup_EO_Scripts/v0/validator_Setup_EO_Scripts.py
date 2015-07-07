#!/usr/bin/env python
import glob
import lsst.eotest.sensor as sensorTest
import lcatr.schema
import siteUtils

sensor_id = siteUtils.getUnitId()

results = []

results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
