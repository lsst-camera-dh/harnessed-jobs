#!/usr/bin/env python
import os
#
# Check for expected environment variables.
#
os.environ['SITENAME']
os.environ['HARNESSEDJOBSDIR']
#
# Check that the package schemas subdir is in the lcatr search path.
#
schema_path = os.environ['LCATR_SCHEMA_PATH']
expected_path = os.path.join(os.environ['HARNESSEDJOBSDIR'], 'schemas')
if expected_path not in schema_path.split(os.path.pathsep):
    raise ValueError('Incorrect LCATR_SCHEMA_PATH: ' + schema_path)
#
# Check for expected modules.
#
import pylab

import lcatr.schema
import lcatr.harness.helpers

import lsst.afw
import lsst.ip.isr

import lsst.eotest

import DataCatalog
import PythonBinding
import ccsTools
import eolib
import eotestUtils
import harnessedJobs
import hdrtools
import siteUtils

results = [siteUtils.packageVersions()]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
