#!/usr/bin/env python
import os
import sys
import subprocess

reb = os.environ["LCATR_UNIT_ID"]

class tsreb_test(object):
    EXEC_TSREB = "source /opt/lsst/setup_tsreb;tsreb_wizard --%s" % reb_id
    def __init__(self, reb_id, remote=None):
        self.remote = remote  
        self.reb_id = int(reb_id)
        if (self.remote != None):
            cmd = "ssh " + self.remote + " " + EXEC_TSREB
        else:
            cmd = EXEC_TSREB

        data_lst = subprocess.check_output(cmd, shell=True)
        data_lst = data_lst.strip()

def do_test():
    import lcatr.schema
    reb_id = os.environ["LCATR_UNIT_ID"]
    reb_id = reb_id.split("-")[1]
    tsp = tsreb_test(reb_id, remote="tsreb@tsreb")

if (__name__ == "__main__"):
    do_test()
