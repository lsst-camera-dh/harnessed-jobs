# harnessed-jobs
Harnessed jobs for running with the eTraveler under the JH

Some environment variables need to be set in addition to the usual set-ups required to run the lcatr code, eotest, LSST stack, etc.:

```
export SITENAME=<location where the jobs are run>
export HARNESSEDJOBSDIR=<full path to this package>
export PYTHONPATH=${HARNESSEDJOBSDIR}/python:${PYTHONPATH}
export LCATR_SCHEMA_PATH=${HARNESSEDJOBSDIR}/schemas:${LCATR_SCHEMA_PATH}
```

`SITENAME` could be, e.g., BNL, Harvard, or SLAC.  The site must have a corresponding folder in the config directory, along with the needed configuration files.

The `LCATR_SCHEMA_PATH` environment variable can alternatively be set by adding a line to the user's lcatr.cfg file:
```
schema_path = <full path to harnessed-jobs package>/schemas
```
The lcatr code will add the directories in that line to its search path for finding the schemas.

For jobs that uses the python/DataCatalog.py module, e.g., SLAC/vendorIngest.py, the path to the datacat module must be added to the python path.  At SLAC, one would do
```
export PYTHONPATH=/afs/slac/u/gl/srs/datacat/dev/0.3/lib:${PYTHONPATH}
```
### Testing the harnessed-jobs set up
To test whether a user's environment is properly set up to run the jobs in this package, one could run the setup_test.py script:
```
$ python ${HARNESSEDJOBSDIR}/tests/setup_test.py
```
This checks for the needed environment variables and imports the needed packages.  An example execution:
```
$ python ../lsst-camera-dh/harnessed-jobs/tests/setup_test.py
Environment variable LCATR_SCHEMA_PATH not found.
Please set this env var or ensure your lcatr.cfg file has the following entry:
schema_path = /nfs/slac/g/ki/ki18/jchiang/LSST/lsst-camera-dh/harnessed-jobs/schemas

The harnessed-jobs set up otherwise appears OK.

Using package versions:
  LSST Stack: 9.2
  eotest: 0.0.0.8-4-gca943b9
  harnessed-jobs: proto-v1.0-109-g1a38479
$
```
There is also a General/harnessed_jobs_setup job that does essentially the same thing that could be added to the start of a process traveler to ensure that the package is properly set up.
