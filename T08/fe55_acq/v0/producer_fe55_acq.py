#!/usr/bin/env python
from ccsTools import ccsProducer
import os

print os.environ

ccsProducer('fe55_acq', 'ccseofe55.py')
