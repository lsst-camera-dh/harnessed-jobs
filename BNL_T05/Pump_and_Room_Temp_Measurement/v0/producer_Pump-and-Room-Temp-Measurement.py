#!/usr/bin/env python
import os
from ccsTools import ccsProducer

#ccsProducer('Pump-and-Room-Temp-Measurement', 'Pump-and-Room-Temp-Measurement.py')
os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/Pump_and_Room_Temp_Measurement/v0/Pump-and-Room-Temp-Measurement.py")
