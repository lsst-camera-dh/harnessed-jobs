#!/usr/bin/env python
import os
import sys
import subprocess

print "The documents received with the hardware will be searched for in the Desktop hardwareReceipt folder"

ccd = os.environ["LCATR_UNIT_ID"]
