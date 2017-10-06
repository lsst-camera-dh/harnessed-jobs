#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os

ccsProducer('RTM_thermal', 'ccsthermal.py')
ccsProducer('RTM_thermal', 'ts7_stats.py')
