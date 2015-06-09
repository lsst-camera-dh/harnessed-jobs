import os
import sys
import lcatr.schema
import harnessedJobs as hj

def getUnitId():
    return os.environ['LCATR_UNIT_ID']

def getCcdVendor():
    unit_id = getUnitId()
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

    result = lcatr.schema.valid(lcatr.schema.get('package_versions'),
                                eotest_version=eotest_version,
                                LSST_stack_version=LSST_stack_version,
                                harnessedJobs_version=hj.getVersion())
    return result
