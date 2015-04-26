import os
import sys

def getJobName():
    """
    Extract the name of the harnessed job assuming standard format for
    the name of the calling script, i.e., [producer,validator]_<jobName>.py.
    """
    # @todo: Use an LCATR env var with this info instead.
    jobName = '_'.join(sys.argv[0].split('_')[1:])[:-3]
    return jobName

def getJobDir():
    """
    Full path of the harnessed job scripts.
    """
    return os.path.join(os.environ['INST_DIR'], getJobName(),
                        os.environ['LCATR_VERSION'])

def jobDirPath(fileName):
    """
    Prepend the job directory to the script filename, thereby giving
    the full path to that script.
    """
    return os.path.join(getJobDir(), fileName)

def getLabName():
    return 'BNL'

def configDir():
    return '.'
