#!/usr/bin/env python
import glob
import lcatr.schema
import os
    
results = []

os.system("cp -vp ~/Desktop/hardwareReceipt/* .")
os.system("chmod 644 *.*")

files = glob.glob('*.*')    
data_products = [lcatr.schema.fileref.make(item) for item in files]
results.extend(data_products)

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
