#!/usr/bin/env python
import glob
import lcatr.schema
import siteUtils

png_files = glob.glob('*.png')
results = [lcatr.schema.fileref.make(item) for item in png_files]
results.extend(siteUtils.jobInfo())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
