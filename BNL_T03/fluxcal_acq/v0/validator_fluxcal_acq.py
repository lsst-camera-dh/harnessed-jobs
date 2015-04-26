#!/usr/bin/env python
from ccsTools import ccsValidator

ccsValidator('fluxcal_acq', statusFlags='stat volt curr pres temp'.split())
