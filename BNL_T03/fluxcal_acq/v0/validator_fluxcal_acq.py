#!/usr/bin/env python
from ccsValidation import ccsValidation

ccsValidation('fluxcal_acq', statusFlags='stat volt curr pres temp'.split())
