#!/usr/bin/env python
import glob
import lcatr.schema
import os

results = []

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
