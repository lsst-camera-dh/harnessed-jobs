#!/usr/bin/env python
import glob
import lcatr.schema
import siteUtils

qe_files = glob.glob('*QE.*')

results = [lcatr.schema.valid(lcatr.schema.get('qe_analysis')),
           siteUtils.packageVersions()]
results.extend([lcatr.schema.fileref.make(item) for item in qe_files])

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
