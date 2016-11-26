import os
import sys
import pickle
import subprocess
import socket
import fnmatch
import ConfigParser
import lcatr.schema
import lcatr.harness.helpers
import harnessedJobs as hj
from eTraveler.clientAPI.connection import Connection
from lcatr.harness.et_wrapper import getHardwareHierarchy


def getCCDNames() :
    topdir = os.getcwd()
    topparts = topdir.split('/')
    activity_id = topparts[len(topparts)-1]
    if not topdir:
        raise RuntimeError, 'cannot determine top-level data directory'
    
# Connect to eTraveler (prod) server with intent to use Dev database
    conn = Connection('homer', 'Dev', prodServer=False)
    if not conn:
        raise RuntimeError, 'unable to authenticate'
    
    ccdnames = {}
    ccdmanunames = {}
    rsp = []
    try:
        rsp = conn.getHardwareHierarchy(experimentSN=getUnitId(),
                                          htype=getUnitType(),
                                          noBatched='false')
        print "Results from getHardwareHierarchy unfiltered:"
        iDict = 0
        for d in rsp:
#            print('Examining array element %d' % (iDict))
            isaccd = False
            ccd_sn = ""
            ccd_slot = ""
            ccd_htype = ""
            ccd_manu_sn = ""
            got_ccd_manu = False
            for k in d:
#                print('For key {0} value is {1}'.format(k, d[k]))
                if ('child_hardwareTypeName' in str(k) and ('itl-ccd' in str(d[k].lower()) or 'e2v-ccd' in str(d[k].lower())) ) :
                    isaccd = True
                    print "found CCD specs"
                if (isaccd and 'child_experimentSN' in str(k)) :
                    ccd_sn = str(d[k])
                    print "CCD SN = %s" % ccd_sn
                if (isaccd and 'slotName' in str(k)) :
                    ccd_slot = str(d[k])
                    print "slot = %s" % ccd_slot
                if (isaccd and 'child_hardwareTypeName' in str(k)) :
                    ccd_htype = str(d[k])
                if (isaccd and ccd_sn != "" and ccd_htype != "" and not got_ccd_manu) :
                    print "trying to get Manufacturer ID for ccd_sn=%s , ccd_htype=%s" % (ccd_sn,ccd_htype)
                    try:
                        ccd_manu_sn = conn.getManufacturerId(experimentSN=ccd_sn,
                                                       htype=ccd_htype)
                        print 'Manufacturer ID: ', ccd_manu_sn
                        got_ccd_manu = True
                    except ValueError,msg:
                        print 'Operation failed with ValueError: ', msg
                    except Exception,msg:
                        print 'Operation failed with exception: '
                        print  msg
                        sys.exit(1)
            iDict +=1
            if (isaccd) :
                ccdnames[ccd_slot] = ccd_sn
                ccdmanunames[ccd_slot] = ccd_manu_sn
    except Exception,msg:
        print 'Operation failed with exception: '
        print  msg
        sys.exit(1)
    
    print "Returning the following list of CCD names and locations"
    print "ccdnames"
    return ccdnames,ccdmanunames

#examining array element 15
#For key child_hardwareTypeName value is ITL-CCD
#For key parent_experimentSN value is LCA-10753_RSA-002_CTE_ETU
#For key level value is 0
#For key relationshipTypeName value is RSA_contains_ITL-CCDs
#For key child_experimentSN value is ITL-NULL5_CTE-ETU
#For key parent_hardwareTypeName value is LCA-10753_RSA
#For key parent_id value is 704
#For key child_id value is 756
#For key slotName value is S20

def cast(value):
    if value == 'None':
        return None
    try:
        if value.find('.') == -1 and value.find('e') == -1:
            return int(value)
        else:
            return float(value)
    except ValueError:
        # Cannot cast as either int or float so just return the
        # value as-is (presumably a string).
        return value

def getUnitId():
    return os.environ['LCATR_UNIT_ID']

def getLSSTId():
    return os.environ['LCATR_UNIT_ID']

def getUnitType():
    return os.environ['LCATR_UNIT_TYPE']

def getRunNumber():
    return os.environ['LCATR_RUN_NUMBER']

def getCcdVendor():
    unit_id = getUnitType()
    vendor = unit_id.split('-')[0]
    if vendor not in ('ITL', 'E2V', 'e2v'):
        raise RuntimeError("Unrecognized CCD vendor for unit id %s" % unit_id)
    return vendor

def getJobName():
    """
    The name of the harnessed job.
    """
    return os.environ['LCATR_JOB']

def getProcessName(jobName=None):
    if jobName is None:
        myJobName = getJobName()
    else:
        myJobName = jobName
    if os.environ.has_key('ET_PROCESS_NAME_PREFIX'):
        return '_'.join((os.environ['ET_PROCESS_NAME_PREFIX'], myJobName))
    else:
        return myJobName

def getJobDir(jobName=None):
    """
    Full path of the harnessed job scripts.
    """
    if jobName is None:
        jobName = getJobName()
    return os.path.join(os.environ['LCATR_INSTALL_AREA'], jobName,
                        os.environ['LCATR_VERSION'])

def jobDirPath(fileName, jobName=None):
    """
    Prepend the job directory to the script filename, thereby giving
    the full path to that script.
    """
    return os.path.join(getJobDir(jobName), fileName)

def getSiteName():
    """
    Return the site or laboratory name
    """
    return os.environ['SITENAME']

def pythonDir():
    """
    Return directory containing the python scripts for this package.
    """
    return os.path.join(os.environ['HARNESSEDJOBSDIR'], 'python')

def configDir():
    """
    Return the full path to the directory containing the site-specific
    configuration files.
    """
    return os.path.join(os.environ['HARNESSEDJOBSDIR'], 'config', getSiteName())

def datacatalog_query(query, folder=None, site=None):
    from DataCatalog import DataCatalog
    if folder is None:
        folder = os.environ['LCATR_DATACATALOG_FOLDER']
    if site is None:
        site = getSiteName()
    datacat = DataCatalog(folder=folder, site=site)
    return datacat.find_datasets(query)

def print_file_list(description, file_list, use_basename=False):
    if description is not None:
        print description
    for item in file_list:
        if use_basename:
            print "  ", os.path.basename(item)
        else:
            print "  ", item
    sys.stdout.flush()

def extractJobId(datacat_path):
    """Extract the eTraveler job ID from the filename path."""
    return int(os.path.basename(os.path.split(datacat_path)[0]))

def datacatalog_glob(pattern, testtype=None, imgtype=None, description=None,
                     sort=False, job_id=None):
    sensor_id = getUnitId()
    if testtype is None or imgtype is None:
        raise RuntimeError("Both testtype and imgtype values must be provided.")
    query = ' && '.join(('LSST_NUM=="%(sensor_id)s"',
                         'TESTTYPE=="%(testtype)s"',
                         'IMGTYPE=="%(imgtype)s"')) % locals()
    datasets = datacatalog_query(query)
    file_lists = {}
    for item in datasets.full_paths():
        if fnmatch.fnmatch(os.path.basename(item), pattern):
            my_job_id = extractJobId(item)
            if not file_lists.has_key(my_job_id):
                file_lists[my_job_id] = []
            file_lists[my_job_id].append(item)
    if job_id is None:
        job_id = max(file_lists.keys())
    file_list = file_lists[job_id]
    if sort:
        file_list = sorted(file_list)
    print_file_list(description, file_list)
    return file_list

def dependency_glob(pattern, jobname=None, paths=None, description=None,
                    sort=False):
    file_list = lcatr.harness.helpers.dependency_glob(pattern, jobname=jobname,
                                                      paths=paths)
    if sort:
        file_list = sorted(file_list)
    print_file_list(description, file_list)
    return file_list

def packageVersions():
    # Not all harnessed jobs will use eotest and/or the LSST Stack, so
    # set 'none' as the default for each.
    try:
        import lsst.eotest
        eotest_version = lsst.eotest.getVersion()
    except ImportError:
        eotest_version = 'none'

    try:
        import lsst.afw
        LSST_stack_version = lsst.afw.__version__
    except ImportError:
        LSST_stack_version = 'none'

    import lcatr.harness.version
    lcatr_harness_version = lcatr.harness.version.__version__

    import lcatr.schema.version
    lcatr_schema_version = lcatr.schema.version.__version__
        
    result = lcatr.schema.valid(lcatr.schema.get('package_versions'),
                                eotest_version=eotest_version,
                                LSST_stack_version=LSST_stack_version,
                                lcatr_harness_version=lcatr_harness_version,
                                lcatr_schema_version=lcatr_schema_version,
                                harnessedJobs_version=hj.getVersion(),
                                hostname=socket.getfqdn())
    return result

def jobInfo():
    results = [packageVersions(), 
               lcatr.schema.valid(lcatr.schema.get('job_info'),
                                  job_name=os.environ['LCATR_JOB'],
                                  job_id=os.environ['LCATR_JOB_ID'])]
    return results

class Parfile(dict):
    def __init__(self, infile, section):
        super(Parfile, self).__init__()
        parser = ConfigParser.ConfigParser()
        parser.read(infile)
        for key, value in parser.items(section):
            self[key] = cast(value)

class DataCatalogMetadata(dict):
    """
    Class to handle metadata passed to the eTraveler for registering
    files with metadata in the Data Catalog.
    """
    def __init__(self, **kwds):
        super(DataCatalogMetadata, self).__init__(**kwds)
    def __call__(self, **kwds):
        my_dict = dict()
        my_dict.update(self)
        my_dict.update(kwds)
        return my_dict

def get_prerequisite_job_id(pattern, jobname=None, paths=None,
                            sort=False):
    """
    Extract the job id of the prerequisite harnesssed job from the
    associated data files (using the dependency_glob pattern),
    assuming that it is included in the folder name.  The Job Harness
    and eTraveler tools do not have a way of providing this
    information, even though the eTraveler db tables do contain it, so
    we are forced to use this ad hoc method.
    """
    files = dependency_glob(pattern, jobname=jobname, paths=paths, sort=sort)
    #
    # The job id is supposed to be the name of the lowest-level folder
    # containing the requested files.
    #
    job_id = os.path.split(os.path.split(files[0])[0])[1]
    return job_id

def get_datacatalog_glob_job_id(pattern, testtype=None, imgtype=None,
                                sort=False):
    """
    Extract the job id of the harnessed job that produced the
    requested data files assuming that it is included in the folder
    name.  Ideally, this information would be in the metadata for
    these files, but it is not so we are forced to use this ad hoc
    method.
    """
    files = datacatalog_glob(pattern, testtype=testtype, imgtype=imgtype,
                             sort=sort)
    #
    # The job id is supposed to be the name of the lowest-level folder
    # containing the requested files.
    #
    job_id = os.path.split(os.path.split(files[0])[0])[1]
    return job_id

def aggregate_job_ids():
    """
    Use lcatr.harness.helpers.dependency_jobids to collect the job ids
    for the harnessed jobs on which the current job depends.  If
    previous dependencies have produced pickle files containing their
    dependency job ids, aggregate them into a common dictionary and
    persist them in a pickle file which downstream jobs can access.
    """
    pickle_file = 'dependency_job_ids.pkl'
    my_dependencies = lcatr.harness.helpers.dependency_jobids()
    prior_job_id_files = lcatr.harness.helpers.dependency_glob(pickle_file)
    if prior_job_id_files:
        for item in prior_job_id_files:
            job_ids = pickle.load(open(item, 'r'))
            if job_ids:
                my_dependencies.update(job_ids)
    pickle.dump(my_dependencies, open(pickle_file, 'w'))
    return my_dependencies

