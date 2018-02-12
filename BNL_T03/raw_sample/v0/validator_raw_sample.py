#!/usr/bin/env python
from ccsTools import ccsValidator
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

file_list = glob("*_rawsample_*.txt")

for idx, f in enumerate(file_list):
    sample_list = np.loadtxt(f)
    plt.plot(sample_list, label=str(idx))

plt.xlabel("sample index")
plt.ylabel("sample value")
plt.title("Raw Sample of all channels")
plt.savefig("rawsample.png")

ccsValidator('raw_sample')
