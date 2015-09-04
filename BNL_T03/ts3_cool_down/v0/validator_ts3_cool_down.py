#!/usr/bin/env python
from ccsTools import ccsValidator
import glob
import lcatr.schema
import os

results = []

lcatr.schema.write_file(results)
lcatr.schema.validate_file()

#ccsValidator('ts3_cool_down_acq')
