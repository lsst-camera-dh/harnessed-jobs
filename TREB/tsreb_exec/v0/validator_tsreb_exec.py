#!/usr/bin/env python
from glob import glob
import os
import subprocess
from collections import OrderedDict

class tsreb_products(object):
    LS_DIR_DATA = "ls -rtd /data/reb* | tail -1"


    def __send_exec__(self):
        if (self.remote != None):
            cmd = "ssh " + self.remote + " " + tsreb_products.LS_DIR_DATA
        else:
            cmd = tsreb_products.LS_DIR_DATA

        data_lst = subprocess.check_output(cmd, shell=True)
        data_lst = data_lst.strip()
        if (len(data_lst) == 0):
            raise Exception("%s: nothing found")

        dirname = os.path.basename(data_lst)
        parsed_dirname = dirname.split("_")
        if (len(parsed_dirname) != 6 and len(parsed_dirname) != 4):
            raise Exception("Bad dirname: %s" % dirname)

        reb_id = int(parsed_dirname[1])
        if (self.reb_id != reb_id):
            raise Exception("REB ID Mismatch! Found %i, need %i" % (reb_id, self.reb_id))

        if (self.remote != None):
            cmd = "scp -rp " + self.remote + ":" + data_lst + " " + os.getcwd()
        else:
            cmd = "cp -rva " + data_lst + " " + os.getcwd()
        exit_code = os.system(cmd)
        if (exit_code != 0):
            raise Exception("Failed to execute: %s", cmd)


    def __call__(self):
        self.__send_exec__()



def do_lcatr():
    import lcatr.schema
    reb_id = os.environ["LCATR_UNIT_ID"]
    reb_id = reb_id.split("-")[1]
    tsp = tsreb_products(reb_id, remote="tsreb@tsreb")
    tsp()


    results = []
    data_products = []
    for item in tsp.get_file_list():
        data_products.append(lcatr.schema.fileref.make(item))

    results.extend(data_products)
    lcat_out = lcatr.schema.valid(lcatr.schema.get('tsreb_upload'), **tsp.get_results_dict())
    results.append(lcat_out)

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()


if (__name__ == "__main__"):
    do_lcatr()
