#!/usr/bin/env python
from ccsTools import ccsProducer
import siteUtils
import os
import sys

for i in range(20) :
     print "This test may be skipped if the REB(s) are(is) already fully powered and you have the authorization. Skip the step (N/y)?"
sys.stdout.flush()
answer = raw_input("\n\nThis test may be skipped if the REB(s) are(is) already fully powered and you have the authorization. Skip the step (N/y)? \n\n")
if "y" in answer.lower() :
     print "Operator requested to skip the step. BYE"
else :
    ccsProducer('rebalive_power', 'ccseorebalive_power.py')

if (False) :
    if "connectivity0" in siteUtils.getJobName() :
        os.system("cp -p ~/c0/* .")
    if "connectivity1" in siteUtils.getJobName() :
        os.system("cp -p ~/c1/* .")
    if "connectivity2" in siteUtils.getJobName() :
        os.system("cp -p ~/c2/* .")
