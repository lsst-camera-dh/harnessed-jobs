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
