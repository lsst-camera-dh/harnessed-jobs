import os
import sys

def getUnitId():
    return os.environ['LCATR_UNIT_ID']

def getJobName():
    """
    The name of the harnessed job.
    """
    return os.environ['LCATR_JOB']

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
