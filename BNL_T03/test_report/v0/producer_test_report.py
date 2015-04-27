#!/usr/bin/env python
import os

#  This is needed so that pylab can write to .matplotlib
os.environ['MPLCONFIGDIR'] = os.curdir
import matplotlib

# For batch-processing, use the AGG backend to avoid needing an X11
# connection.
matplotlib.use('Agg')

import json
import pylab
import lsst.eotest.sensor as sensorTest
from lcatr.harness.helpers import dependency_glob
import siteUtils

class JsonRepackager(object):
    _key_map = dict((('gain', 'GAIN'),
                     ('psf_sigma', 'PSF_SIGMA'),
                     ('read_noise', 'READ_NOISE'),
                     ('bright_pixels', 'NUM_BRIGHT_PIXELS'),
                     ('bright_columns', 'NUM_BRIGHT_COLUMNS'),
                     ('dark_pixels', 'NUM_DARK_PIXELS'),
                     ('dark_columns', 'NUM_DARK_COLUMNS'),
                     ('dark_current_95CL', 'DARK_CURRENT_95'),
                     ('num_traps', 'NUM_TRAPS'),
                     ('cti_serial', 'CTI_SERIAL'),
                     ('cti_parallel', 'CTI_PARALLEL'),
                     ('full_well', 'FULL_WELL'),
                     ('max_frac_dev', 'MAX_FRAC_DEV'),
                     ))
    def __init__(self, outfile='eotest_results.fits'):
        """
        Repackage per amp information in the json-formatted 
        summary.lims files from each analysis task into the
        EOTestResults-formatted output.
        """
        self.eotest_results = sensorTest.EOTestResults(outfile)
    def process_file(self, infile):
        foo = json.loads(open(infile).read())
        for result in foo:
            if result.has_key('amp'):
                amp = result['amp']
                for key, value in result.items():
                    if key.find('schema') == 0 or key == 'amp':
                        continue
                    self.eotest_results.add_seg_result(amp, self._key_map[key],
                                                       value)
    def write(self, outfile=None, clobber=True):
        self.eotest_results.write(outfile=outfile, clobber=clobber)

sensor_id = siteUtils.getUnitId()

# Aggregate information from summary.lims files into
# a final EOTestResults output file.
repackager = JsonRepackager()
summary_files = dependency_glob('summary.lims')
for item in summary_files:
    repackager.process_file(item)
results_file = '%s_eotest_results.fits' % sensor_id
repackager.write(results_file)

plots = sensorTest.EOTestPlots(sensor_id, results_file=results_file)

# Fe55 flux distribution fits
fe55_file = dependency_glob('%s_psf_results*.fits' % sensor_id,
                            jobname='fe55_analysis')[0]
plots.fe55_dists(fe55_file=fe55_file)
pylab.savefig('%s_fe55_dists.png' % sensor_id)

# PSF distributions from Fe55 fits
plots.psf_dists(fe55_file=fe55_file)
pylab.savefig('%s_psf_dists.png' % sensor_id)

# Photon Transfer Curves
ptc_file = dependency_glob('%s_ptc.fits' % sensor_id, jobname='ptc')[0]
plots.ptcs(ptc_file=ptc_file)
pylab.savefig('%s_ptcs.png' % sensor_id)

# Linearity plots
detresp_file = dependency_glob('%s_det_response.fits' % sensor_id,
                               jobname='flat_pairs')[0]
plots.linearity(ptc_file=ptc_file, detresp_file=detresp_file)
pylab.savefig('%s_linearity.png' % sensor_id)

# System Gain per segment
plots.gains()
pylab.savefig('%s_gains.png' % sensor_id)

# Read Noise per segment
plots.noise()
pylab.savefig('%s_noise.png' % sensor_id)

# Quantum Efficiency
qe_file = dependency_glob('*%s_QE.fits' % sensor_id, jobname='qe_analysis')[0]
plots.qe(qe_file=qe_file)
pylab.savefig('%s_qe.png' % sensor_id)

# Crosstalk matrix
xtalk_file = dependency_glob('*%s_xtalk_matrix.fits' % sensor_id,
                             jobname='crosstalk')[0]
plots.crosstalk_matrix(xtalk_file=xtalk_file)
pylab.savefig('%s_xtalk.png' % sensor_id)

# Flat fields at wavelengths nearest the centers of the standard bands
wl_files = dependency_glob('*_lambda_*.fits', jobname='qe_acq')
print wl_files
wl_file_path = os.path.split(wl_files[0])[0]
plots.flat_fields(wl_file_path)
pylab.savefig('%s_flat_fields.png' % sensor_id)

# Create the test report pdf.
report = sensorTest.EOTestReport(plots, wl_file_path)
report.make_pdf()

