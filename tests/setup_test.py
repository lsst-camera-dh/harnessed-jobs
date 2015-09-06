import os
eobj = None
try:
    #
    # Check for expected environment variables.
    #
    os.environ['SITENAME']
    os.environ['HARNESSEDJOBSDIR']
    try:
        schema_path = os.environ['LCATR_SCHEMA_PATH']
        expected_path = os.path.join(os.environ['HARNESSEDJOBSDIR'], 'schemas')
        if expected_path not in schema_path.split(os.path.pathsep):
            raise ValueError('Incorrect LCATR_SCHEMA_PATH: ' + schema_path)
    except KeyError:
        print 'Environment variable LCATR_SCHEMA_PATH not found.'
        print 'Please set this env var or ensure your lcatr.cfg file has the following entry:'
        print 'schema_path = %s/schemas\n' % os.environ['HARNESSEDJOBSDIR']
    #
    # Check for expected modules.
    #
    import pylab
    
    import lcatr.schema
    import lcatr.schema.version
    import lcatr.harness.helpers
    import lcatr.harness.version

    import lsst.afw
    import lsst.ip.isr

    import lsst.eotest

    import DataCatalog
    import PythonBinding
    import ccsTools
    try:
        import eolib
    except ImportError, eobj:
        print "Error importing eolib:"
        print eobj
        
    import eotestUtils
    import harnessedJobs
    import hdrtools
    import siteUtils

    if 'schema_path' in locals() and eobj is None:
        print "The harnessed-jobs set up appears OK."
    else:
        print "The harnessed-jobs set up otherwise appears OK."
    print
    print "Using package versions:"
    print "  LSST Stack:", lsst.afw.__version__
    print "  lcatr.harness:", lcatr.harness.version.__version__
    print "  lcatr.schema:", lcatr.schema.version.__version__
    print "  eotest:", lsst.eotest.getVersion()
    print "  harnessed-jobs:", harnessedJobs.getVersion()
except Exception, eobj:
    print "The harnessed-jobs package has not been set up correctly."
    print
    if type(eobj) == KeyError:
        print "Missing environment variable:", eobj
    elif type(eobj) == ImportError:
        print "ImportError:", eobj
    else:
        raise eobj
