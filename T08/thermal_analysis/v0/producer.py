#!/usr/bin/env python
import Tkinter
import glob
import shutil
import os
import matplotlib.pyplot as plt
import ccs_trending
import siteUtils
import time
import subprocess

raft_id = siteUtils.getLSSTId()
run_number = siteUtils.getRunNumber()

host = 'localhost'

jobDir = siteUtils.getJobDir()

shutil.copy("%s/ts_quantities.cfg" % jobDir ,os.getcwd())
shutil.copy("%s/ts8_quantities.cfg" % jobDir ,os.getcwd())

ccsProducer('RTM_thermo', 'ccsthermal.py')

cdir = os.getcwd()

#rtmstatelist = [
#"RTM_off_5min_stable__502",
#"REB_quiescient_record__505",
#"RTM_quies_5min_record__508",
#"RTM_biases_5min_record__510",
#"RTM_clears_5min_record__512",
#"RSA_0_5min_record__514",
#"RSA_50_5min_record__516",
#"RSA_100_5min_record__518",
#"RTM_quies_5min_record__520"
#]


rtmstatelist = [
"RTM_off_stable_state__501",
"REB_quiescient_30min_stable__504",
"RTM_quies_stable__507",
"RTM_thermal_biases_htr_0__509",
"RTM_thermal_clear_htr_0__511",
"RSA_0__513",
"RSA_50__515",
"RSA_100__517",
"RTM_quies_stable__519",
]


sectionlist = [
"Temp_a_to_d",
"Plate_Heaters",
"REB0_temperatures",
"REB0_powers",
"REB0_clocks",
"REB1_temperatures",
"REB1_powers",
"REB1_clocks",
"REB2_temperatures",
"REB2_powers",
"REB2_clocks"
]



tm = time.time()
#start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-300))
#end = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm))

for rtmstate in rtmstatelist :

    tempfile = "/home/ts8prod/jobHarness/jh_stage/LCA-11021_RTM/%s/%s/%s/v0/*/2*.log" % (raft_id,run_number,rtmstate)                                    
    print "test - ",subprocess.check_output('egrep -h \"step \\"produce\" %s ' % tempfile, shell=True)
    rstart = subprocess.check_output('egrep -h "step \\"produce" %s | awk \'{print $1,substr($2,1,index($2,",")-1)}\' | tail -1' % tempfile, shell=True)
    rstop = subprocess.check_output('egrep -h "produce completed" %s | awk \'{print $1,substr($2,1,index($2,",")-1)}\' | tail -1' % tempfile, shell=True)

    print "rstart",rstart
    print "rstop",rstop

    ristart = time.strptime(rstart.strip(),'%Y-%m-%d %H:%M:%S')
    ristop = time.strptime(rstop.strip(),'%Y-%m-%d %H:%M:%S')

    tm = time.mktime(ristop)
    start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-330))

    end = time.strftime('%Y-%m-%dT%H:%M:%S',ristop-30)
    
    
    ccs_subsystem = 'ts'

    config_file = 'ts_quantities.cfg'
    
    time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1)
    config = ccs_trending.ccs_trending_config(config_file)
    for section in config.sections():
        plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                               time_axis=time_axis)
        plotter.read_config(config, section)
        title = "%s, %s, %s" % (raft_id, run_number, section)
        plotter.plot(title=title)
        plt.savefig('%s_%s_%s_%s.png' % (rtmstate, section, raft_id, run_number))
        plotter.save_file('%s_%s_%s_%s.txt' % (rtmstate, section, raft_id, run_number))
    
    
    try:
    
        ccs_subsystem = 'ts8'
        
        config_file = 'ts8_quantities.cfg'
        
        time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1)
        config = ccs_trending.ccs_trending_config(config_file)
        for section in config.sections():
            plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                                   time_axis=time_axis)
            plotter.read_config(config, section)
            title = "%s, %s, %s" % (raft_id, run_number, section)
            plotter.plot(title=title)
            plt.savefig('%s_%s_%s_%s.png' % (rtmstate, section, raft_id, run_number))
            plotter.save_file('%s_%s_%s_%s.txt' % (rtmstate, section, raft_id, run_number))
    except:
        pass

print
print " ----------------------------------------------------------------------------------------"
print

fp = open("%s/%s_raw_inputs.txt" % (cdir,raft_id),"w");

for rtmstate in rtmstatelist :
    fp.write("\n\n========== RTM state descriptor: %s =======\n" % rtmstate)
    for sec in sectionlist :
        statfile = '%s/%s_%s_%s_%s.txt' % (cdir,rtmstate,sec,raft_id,run_number)

        try :
            fp2 = open(statfile,"r")
            for line in fp2 :
                fp.write("%s %s" % (rtmstate,line))
            fp2.close()
        except :
            pass

fp.close()
