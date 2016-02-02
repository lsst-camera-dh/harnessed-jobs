#!/usr/bin/env python
import os
import glob
import shutil
import lcatr.schema
import siteUtils
import eotestUtils

sensor_id = siteUtils.getUnitId()
results_file = '%s_eotest_results.fits' % sensor_id
eotestUtils.addHeaderData(results_file, LSST_NUM=sensor_id,
                          DATE=eotestUtils.utc_now_isoformat(),
                          CCD_MANU=siteUtils.getCcdVendor().upper())
results = [lcatr.schema.fileref.make(results_file)]

png_files = glob.glob('*.png')
results.extend([lcatr.schema.fileref.make(item) for item in png_files])

test_report = '%s_eotest_report.pdf' % sensor_id
results.append(lcatr.schema.fileref.make(test_report))

results.extend(siteUtils.jobInfo())

#
# CCS configuration files
#
config_dir = siteUtils.configDir()
ccs_configs = os.path.join(config_dir, 'acq.cfg')
shutil.copy(ccs_configs, '.')
results.append(lcatr.schema.fileref.make(os.path.basename(ccs_configs)))
for line in open(ccs_configs):
    if line.find('=') == -1:
        continue
    tokens = line.strip().split('=')
    filename = os.path.join(config_dir, tokens[1].strip())
    shutil.copy(filename, '.')
    results.append(lcatr.schema.fileref.make(os.path.basename(filename)))

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
