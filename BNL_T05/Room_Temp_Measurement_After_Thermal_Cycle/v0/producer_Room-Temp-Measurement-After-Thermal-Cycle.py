#!/usr/bin/env python
import os
from ccsTools import ccsProducer

#ccsProducer('Room-Temp-Measurement-After-Thermal-Cycle', 'Room-Temp-Measurement-After-Thermal-Cycle.py')
os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/Room_Temp_Measurement_After_Thermal_Cycle/v0/Room-Temp-Measurement-After-Thermal-Cycle.py")
