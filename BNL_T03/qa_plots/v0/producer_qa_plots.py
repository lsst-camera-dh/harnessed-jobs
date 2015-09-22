#!/usr/bin/env python
import os
from collections import OrderedDict

#  This is needed so that pylab can write to .matplotlib
os.environ['MPLCONFIGDIR'] = os.curdir

# For batch-processing, use the AGG backend to avoid needing an X11
# connection.
import matplotlib
matplotlib.use('Agg')

from lcatr.harness.helpers import dependency_glob
import siteUtils
from eo_acq_qa import TrendingObjects

def dirname_dependencyGlob(sensor_id, **kwds):
    """
    Return the directory path with the FITS output files for the
    specified jobname.
    """
    if kwds.has_key('jobname'):
        kwds['jobname'] = siteUtils.getProcessName(kwds['jobname'])
    file0 = dependency_glob('%(sensor_id)s*.fits' % locals(), **kwds)[0]
    dirname = os.path.split(file0)[0]
    if dirname == '':
        dirname = '.'
    return dirname

sensor_id = siteUtils.getUnitId()

datasets = OrderedDict([('FE55', 'fe55_acq'),
                        ('DARK', 'dark_acq'),
                        ('FLAT', 'flat_acq'),
                        ('PPUMP', 'ppump_acq'),
                        ('SFLAT', 'sflat_acq'),
                        ('QE', 'qe_acq'),
                        ('PERSISTENCE', 'persist_acq')])

QA_trender = TrendingObjects()
for test_type, jobname in datasets.items():
    dirname = dirname_dependencyGlob(sensor_id, jobname=jobname)
    QA_trender.processDirectory(dirname, test_type)
QA_trender.plot(sensor_id)
