#!/usr/bin/env python
import glob
import lcatr.schema
import os
import siteUtils

results = []
#ccd = os.environ["LCATR_UNIT_ID"]
#topccddir = "/cygdrive/c/DATA/%s" % ccd
#ccddir = "%s/%s" % (topcddir,time.strftime("%Y%m%d-%H:%M:%S"))

#os.system("cp -vp %s/* ." % cddir)
#os.system("chmod 644 *.*")


files = siteUtils.dependency_glob('dlink/*.*',
                                  jobname=siteUtils.getProcessName('Make-OGP-Directories'),
                                  description='OGP result files:')
#files = glob.glob('*.*')    
data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

for item in files :
    print "Archiving file - %s" % item

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
