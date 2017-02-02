#!/usr/bin/env python
from ccsTools import ccsProducer
import siteUtils
import os


ccsProducer('rebalive_power', 'ccseorebalive_power.py')
if (False) :
    if "connectivity0" in siteUtils.getJobName() :
        os.system("cp -p ~/c0/* .")
    if "connectivity1" in siteUtils.getJobName() :
        os.system("cp -p ~/c1/* .")
    if "connectivity2" in siteUtils.getJobName() :
        os.system("cp -p ~/c2/* .")
