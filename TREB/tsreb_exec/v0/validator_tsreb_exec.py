#!/usr/bin/env python
from glob import glob
import os
import subprocess
import lcatr.schema

results = []
tsrebfiles = glob("*log*")
data_products = [lcatr.schema.fileref.make(item) for item in tsrebfiles]
results.extend(data_products)
lcatr.schema.write_file(results)
lcatr.schema.validate_file()

