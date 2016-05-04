#!/usr/bin/env python
import os
import sys
import shutil
from collections import OrderedDict

#  This is needed so that pylab can write to .matplotlib
os.environ['MPLCONFIGDIR'] = os.curdir
import matplotlib

# For batch-processing, use the AGG backend to avoid needing an X11
# connection.
matplotlib.use('Agg')

import json
import pyfits
import pylab
from lcatr.harness.helpers import dependency_glob
import siteUtils

def processName_dependencyGlob(*args, **kwds):
    if kwds.has_key('jobname'):
        kwds['jobname'] = siteUtils.getProcessName(kwds['jobname'])
    return dependency_glob(*args, **kwds)


reb_id = siteUtils.getUnitId()
results_file = '%s_rebtest_results.fits' % reb_id

power_files = processName_dependencyGlob('*.fits', jobname='rebalive_power')
func_files = processName_dependencyGlob('*.fits', jobname='rebalive_functinality')

# reb power plots
plots.power()
pylab.savefig('%s_power.png' % reb_id)

# reb functionality plots
plots.functionality()
pylab.savefig('%s_power.png' % reb_id)


# Create the test report pdf.
report = rebTest.Report(plots, wl_file_path,
                                 power_plot_files=power_plot_files,
                                 func_plot_files=func_plot_files)

report.make_pdf()

