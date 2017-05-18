#!/usr/bin/env python
from glob import glob
import os
import subprocess
from collections import OrderedDict

class tsreb_products(object):
    LS_DIR_DATA = "ls -rtd /data/reb*%s* | tail -1"

    def __init__(self, reb_id, remote=None):
        self.remote = remote    # "tsreb@130.199.47.42"
        self.reb_id = int(reb_id)

    def __parse_version_file__(self, ver_file):
        f = open(ver_file, "r")
        ret_dict = OrderedDict()

        for l in f.readlines():
            lsplit = l.split(": ")
            if (len(lsplit) != 2):
                raise Exception("ERROR: Invalid version file format")
            ret_dict["version_" + lsplit[0]] = lsplit[1].strip()           

        return ret_dict

    def __parse_tex_file__(self, tex_file):
        f = open(tex_file, "r")
        summary_table = []
        in_table = False
        in_section = False

        for l in f.readlines():
            if ("\\bottomrule" in l and in_table and in_section):
                break

            if (in_section and in_table):
                summary_table.append(l.strip())

            if ("\section{Summary}" in l):
                in_section = True
            elif (in_section and "\midrule" in l):
                in_table = True

        f.close()
        ret_dict = OrderedDict()
        for l in summary_table:
            results = l.split("&")
            passfail = results[0].split(" ")[1].strip("\'")
            measurment = results[1]
            measurment = measurment.replace("{", "").replace("}", "")
            ret_dict[measurment] = passfail

        return ret_dict

    def __get_files__(self):
        if (self.remote != None):
            cmd = "ssh " + self.remote + " " + tsreb_products.LS_DIR_DATA % self.reb_id
        else:
            cmd = tsreb_products.LS_DIR_DATA % self.reb_id

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

        print cmd
        exit_code = os.system(cmd)
        if (exit_code != 0):
            raise Exception("Failed to execute: %s", cmd)

        self.pdf_report = glob(dirname+"/*.pdf")
        self.raw_data   = glob(dirname+"/data/*.csv")
        self.raw_data.extend(glob(dirname+"/data/*.fits"))
        self.tsreb_version = glob(dirname+"/data/*VERSION*")[0]
        self.tex_file = glob(dirname+"/data/*.tex")[0]

    def __call__(self):
        self.__get_files__()

    def write_schema(self, version, fname="tsreb_upload.schema", schema_name="tsreb_upload"):
        schema_dict = self.get_results_dict()

        f = open(fname, "w")
        f.write("# -*- python -*-\n{\n")
        f.write("    'schema_name' : '" + schema_name + "',\n")
        f.write("    'schema_version' : " + str(version) + ",\n")
        for k in schema_dict.keys():
            s = "    "
            s += "\'" + str(k) + "\'"
            s += " : "
            s += "str,\n"
            f.write(s)

        f.write("}\n\n")
        f.flush()
        f.close()

    def get_results_dict(self):
        res_dict = self.__parse_tex_file__(self.tex_file)
	res_dict.update(self.__parse_version_file__(self.tsreb_version))
        return res_dict

    def get_file_list(self):
        lst = self.pdf_report
        lst.extend(self.raw_data)
        #lst.extend(self.tsreb_version)
        return lst

def do_lcatr():
    import lcatr.schema
    reb_id = os.environ["LCATR_UNIT_ID"]
    if (len(reb_id.split("-")) != 3):
        raise Exception("ERROR: Invalid REB ID format: %s" % (reb_id))
	return

    remote = None
    if (os.environ.has_key('TSREB_SSH_LOGIN')):
	remote = os.environ('TSREB_SSH_LOGIN')

    reb_id = reb_id.split("-")[2]
    tsp = tsreb_products(reb_id, remote=remote)
    tsp()
    tsp.write_schema(0, fname="%s/TREB/tsreb_upload/v0/tsreb_upload.schema" % os.environ['HARNESSEDJOBSDIR'])

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
#    tsp = tsreb_products(4, remote="jkuczewski@tsreb")
#    tsp()

#    print tsp.get_results_dict()
#    print tsp.get_file_list()
#    tsp.write_schema(0)


