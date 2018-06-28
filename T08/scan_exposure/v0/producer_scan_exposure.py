#!/usr/bin/env python
from ccsTools import ccsProducer
import os

os.system('ts7VQMoff')
ccsProducer('scan_exposure', 'ccsscan_exposure.py')
os.system('ts7VQMon')
if (False) :
    os.system("cp -p ~/ex0/* .")
