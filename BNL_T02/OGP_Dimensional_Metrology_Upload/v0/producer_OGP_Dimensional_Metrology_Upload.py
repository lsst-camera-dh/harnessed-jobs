#!/usr/bin/env python
import os
import sys
import subprocess

os.system("rsync -r LSSTuser@172.17.100.2:/cygdrive/c/Production_DATA /home/LSSTuser/OGP_mirror/cygdrive/c/")
