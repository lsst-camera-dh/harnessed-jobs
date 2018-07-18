#!/usr/bin/env python
import os
from ccsTools import ccsProducer

#ccsProducer('Keyence_Calibration', 'Keyence_Calibration.py')
os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/Keyence_Calibration/v0/Keyence_Calibration.py")
