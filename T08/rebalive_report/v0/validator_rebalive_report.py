#!/usr/bin/env python
import os
import glob
import shutil
import lcatr.schema
import siteUtils
import eotestUtils

reb_id = siteUtils.getUnitId()


png_files = glob.glob('*.png')
results.extend([lcatr.schema.fileref.make(item,
                                          metadata=md(DATA_PRODUCT=eotestUtils.png_data_product(item, sensor_id)))
                for item in png_files])

test_report = '%s_rebtest_report.pdf' % sensor_id
results.append(lcatr.schema.fileref.make(test_report,
                                         metadata=md(DATA_PRODUCT='REBTEST_REPORT')))

results.extend(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
