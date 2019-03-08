#!/usr/bin/env python
import os
from ccsTools import ccsProducer

#ccsProducer('Cooling-Measurement-2', 'Cooling-Measurement-2.py')
os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/Cooling_Measurement-2/v0/Cooling-Measurement-2.py")
