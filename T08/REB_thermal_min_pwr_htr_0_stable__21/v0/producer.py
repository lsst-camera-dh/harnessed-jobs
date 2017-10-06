#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os

ccsProducer('RTM_thermal_powered', 'ccsthermal.py')
ccsProducer('RTM_thermal_powered', 'ts7_stats.py')
