import os
import glob
import subprocess
import lcatr.schema
from hdrtools import updateFitsHeaders
import siteUtils
    
def ccsValidation(jobName, acqfilelist='acqfilelist'):
    updateFitsHeaders(acqfilelist)

    # @todo Implement trending plot generation using python instead of
    # using gnuplot
    sitedir = os.path.join(os.environ['VIRTUAL_ENV'], "TS3_JH_acq", "site")
    subprocess.call(os.path.join(sitedir, "dotemppressplots.sh"), shell=True)

    results = []
    tsstat = open("status.out").readline()
    results.append(lcatr.schema.valid(lcatr.schema.get(jobName), stat=tsstat))

    # @todo Fix this. Copying these files should not be necessary.
    jobdir = siteUtils.getJobDir()
    os.system("cp -vp %s/*.fits ." % jobdir)   

    # @todo Sort out which files really need to be curated.
    files = glob.glob('*.fits,*values*,*log*,*summary*,*.dat,*.png,bias/*.fits')
    data_products = [lcatr.schema.fileref.make(item) for item in files]
    results.extend(data_products)

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()
