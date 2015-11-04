import argparse
from DataCatalog import *


## Command line arguments
parser = argparse.ArgumentParser(description='Find archived data in the LSST  data Catalog. These include CCD test stand and vendor data files.')

## FT1 metadata filter opts
parser.add_argument('-f','--filter',default=None,help="FT1 metadata filter string (default=%(default)s)")
##   The following are 'convenience options' which could also be specified in the filter string
parser.add_argument('-t','--timestamp',default=None,help="(metadata) File timestamp (default=%(default)s)")
parser.add_argument('-s','--sensorID', default=None,help="(metadata) Sensor ID (default=%(default)s)")
parser.add_argument('-T','--TestName', default='',help="(metadata) test type (default=%(default)s)")
parser.add_argument('-c','--CCDType', default="ITL",help="(metadata) CCD vendor type (default=%(default)s)")
parser.add_argument('-S','--site', default="slac.lca.archive",help="File location (default=%(default)s) ")
parser.add_argument('-F','--FType', default='',help="File type (default all) ")
parser.add_argument('-q','--qType', default='',help="query type - report or blank (default all) ")

## Limit dataCatalog search to specified parts of the catalog
parser.add_argument('-g','--group',default=None,help="Limit search to specified dataCat group (default=%(default)s)")
parser.add_argument('-m','--mirrorName',default='BNL-test',help="mirror name to search, i.e. in dataCat /LSST/mirror/<mirrorName> (default=%(default)s)")
parser.add_argument('-X','--XtraOpts',default='',help="any extra 'datacat find' options (default=%(default)s)")

## Output
parser.add_argument('-o','--outputFile',default=None,help="Output result to specified file (default = %(default)s)")
parser.add_argument('-a','--displayAll',default=False,action='store_true',help="Display entire result set (default = %(default)s)")

## Verbosity
parser.add_argument('-d','--debug',default=False,action='store_true',help="enable debug mode (default=%(default)s)")
parser.add_argument('-x','--dryRun',default=False,action='store_true',help="dry run (no DB action) (default=%(default)s)")

args = parser.parse_args()

sensorID = args.sensorID

sourceMap = {
        'BNL-prod': 'BNL-prod/prod/',
        'BNL-test': 'BNL-test/test/',
        'vendorCopy-prod': 'SLAC-prod/prod/',
        'vendorCopy-test': 'SLAC-test/test/',
        'vendor-prod': 'vendorData/',
        'vendor-test': 'vendorData/',
	'SAWG-BNL': 'BNL-SAWG/SAWG/'
        }
    
folder = '/LSST/'

use_latest_activity = True

if (args.mirrorName == 'BNL-prod' or args.mirrorName == 'BNL-test'):
        folder = folder + 'mirror/' + sourceMap[args.mirrorName] + args.CCDType + '-CCD/' + sensorID + '/'
	if args.TestName != '':
		folder += args.TestName + '/v0/'
	else:
		use_latest_activity = False
elif (args.mirrorName == 'vendorCopy-prod' or args.mirrorName == 'vendorCopy-test'):
        folder = folder + 'mirror/' + sourceMap[args.mirrorName] + args.CCDType + '-CCD/' + sensorID
	if args.TestName != '':
		folder += '/' + args.TestName + '/v0/'
	elif args.qType == '':
		folder += '/vendorIngest/v0/'
	else:
		folder += '/test_report_offline/v0/'
elif (args.mirrorName == 'vendor-prod'):
        folder = folder + sourceMap[args.mirrorName] + args.CCDType  + '/' + sensorID + '/Prod/'
elif (args.mirrorName == 'vendor-test'):
        folder = folder + sourceMap[args.mirrorName] + args.CCDType  + '/' + sensorID + '/Dev/'
elif (args.mirrorName == 'SAWG-BNL'):
        folder = folder + 'mirror/' + sourceMap[args.mirrorName] + args.CCDType  + '/' + sensorID + '/' + args.TestName
	use_latest_activity = False
        

print folder
        
query = args.XtraOpts

site = args.site

datacatalog = DataCatalog(folder=folder, experiment='LSST', site=site, use_newest_subfolder=use_latest_activity)

datasets = datacatalog.find_datasets(query)
print "%i datasets found\n" % len(datasets)

nfiles = 75
print "Requested ftype - " + args.FType
if args.debug:
        print "File paths for first %i files at %s:" % (nfiles, site)
        for item in datasets.full_paths()[:nfiles]:
		if (args.FType == '') or (args.FType != '' and item.endswith(args.FType)): 
		    print item

print

## Write file with list of found data files, if requested
if args.outputFile != None and len(datasets)>0:
        print 'Writing output file ',args.outputFile,'...'
        ofile = open(args.outputFile,'w')
        for line in datasets.full_paths():
	    if (args.FType == '') or (args.FType != '' and line.endswith(args.FType)): 
		    ofile.write(line+'\n')
            pass
        ofile.close()
elif args.outputFile != None:
        print "Result file requested, but no files found"
        pass


#datasets.download(dryrun=args.dryRun, clobber=False, nfiles=nfiles)
