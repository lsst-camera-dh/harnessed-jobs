#!/usr/bin/env python
import os
from ccsTools import ccsProducer

#ccsProducer('Cold-Measurement', 'Cold-Measurement.py')
os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/Cold_Measurement/v0/Cold-Measurement.py")
