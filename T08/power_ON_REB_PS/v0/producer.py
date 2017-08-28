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
    ccsProducer('power_ON_REB', 'ccs_power_ON_REB_PS.py')
