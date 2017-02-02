#!/usr/bin/env python
from ccsTools import ccsProducer
import os

ccsProducer('rebalive_exposure', 'ccseorebalive_exposure.py')
if (False) :
    os.system("cp -p ~/ex0/* .")
