#!/usr/bin/env python

import numpy as np
from scipy.interpolate import interp1d

class PdSens(object):
    def __init__(self, sensfile='hamamatsu_pd_cal.csv'):
        self.data = np.recfromcsv(sensfile, names='wl, sens', skip_header=1)
        self.func = interp1d(self.data['wl'], self.data['sens'])
    def __call__(self, wl):
        return self.func(wl)

def make_ratio_file(infile, outfile, pd_area=1.05e-4,
                    pd_sens_file='hamamatsu_pd_cal.csv'):
    pd_sens = PdSens(pd_sens_file)
    data = np.recfromcsv(infile, names='wl, pd_cal, pd_mon, pd_ratio',
                         skip_header=1)

    header = " wl(nm)  cal_pd_sens(A/W)   pd_ratio\n"

    output = open(outfile, 'w')
    output.write('pd_area = %.3e\n' % pd_area)
    output.write(header)
    for wl, pd_cal, pd_mon, pd_ratio in data:
        try:
            output.write(' %.1f      %.5f         %.3e\n'
                         % (wl, pd_sens(wl), pd_ratio))
        except ValueError:
            pass
    output.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert TS3 photodiode calibration data to a format expected by the eotest QE analysis.')
    parser.add_argument('infile', help='Wavelength scan of monitoring diode and calibration diode measurements')
    parser.add_argument('outfile', help='Output file name')
    parser.add_argument('--pd_area', type=float, default=1.05e-4,
                        help='Collecting area of calibration photodiode (mm^2)')
    parser.add_argument('--pd_sens_file', type=str,
                        default='hamamatsu_pd_cal.csv',
                        help='Absolute sensitivity for calibration photodiode')

    args = parser.parse_args()

    make_ratio_file(args.infile, args.outfile, pd_area=args.pd_area,
                    pd_sens_file=args.pd_sens_file)
    
