import os
import sys

def getJobName():
    """
    Extract the name of the harnessed job assuming standard format for
    the name of the calling script, i.e.,
    [producer,validator]_<jobName>.py.
    """
    # @todo: Use an LCATR env var with this info instead.
    jobName = '_'.join(sys.argv[0].split('_')[1:])[:-3]
    return jobName

def getJobDir(jobName=None):
    """
    Full path of the harnessed job scripts.
    """
    if jobName is None:
        jobName = getJobName()
    return os.path.join(os.environ['INST_DIR'], jobName,
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
    return return os.environ['SITENAME']

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
