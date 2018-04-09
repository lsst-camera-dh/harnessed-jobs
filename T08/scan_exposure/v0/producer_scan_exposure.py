#!/usr/bin/env python
from ccsTools import ccsProducer
import os

ccsProducer('scan_exposure', 'ccsscan_exposure.py')
if (False) :
    os.system("cp -p ~/ex0/* .")
