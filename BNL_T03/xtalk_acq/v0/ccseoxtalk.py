###############################################################################
# xtalk
#    script for doing crosstalk acq
#
###############################################################################

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

try:
    pass
except:
    raise RuntimeError("Exception raised during xtalk_acq at time %f" % time.time())

print "ccseoxtalk finished."
