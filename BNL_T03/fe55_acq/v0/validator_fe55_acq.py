#!/usr/bin/env python
import os
import glob
import subprocess
import lcatr.schema
import hdrtools as ht
import siteUtils
    
#
# Update FITS file headers.
#
for line in open("acqfilelist", "r"):
    tokens = str.split(line)
    fitsfile = tokens[0]
    pdfile = tokens[1]
    tstamp = tokens[2]
    try:
        ht.addPDvals(fitsfile, pdfile, "AMP0.MEAS_TIMES", "AMP0", tstamp)
    except:
        raise RuntimeError("Problem in addPDvals. Check that %s was created. " % fitsfile)
    try:
        print ht.fitsAverage(fitsfile)
    except:
        raise RuntimeError("Problem in fitsAverage. Check that %s was created. " % fitsfile)
    try:
        ht.hdrsummary(fitsfile, "summary.txt")
    except:
        raise RuntimeError("Problem in hdrsummary. Check that %s was created. " % fitsfile)

#
# @todo Implement trending plot generation using python instead of using gnuplot
#
sitedir = os.path.join(os.environ['VIRTUAL_ENV'], "TS3_JH_acq", "site")
subprocess.call(os.path.join(sitedir, "dotemppressplots.sh"), shell=True)

results = []
tsstat = open("status.out").readline()
results.append(lcatr.schema.valid(lcatr.schema.get('fe55_acq'), stat=tsstat))

jobdir = siteUtils.getJobDir()
os.system("cp -vp %s/*.fits ." % jobdir)   # @todo Fix this. Copying should not be necessary.

# @todo Sort out which files really need to be curated.
files = glob.glob('%s/*.fits,*values*,*log*,*summary*,*.dat,*.png,bias/*.fits' % os.getcwd())
data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
