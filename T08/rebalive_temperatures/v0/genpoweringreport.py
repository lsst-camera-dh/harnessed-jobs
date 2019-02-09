#!/usr/bin/env python
import Tkinter
import glob
import shutil
import os
import matplotlib.pyplot as plt
import ccs_trending
import time
import subprocess

host = 'localhost'

run_number = 0
cdir = os.getcwd()

test_id = str(int(time.time()))


sectionlist = [
"REB0_currents",
"REB0_clocks",
"REB1_currents",
"REB1_clocks",
"REB2_currents",
"REB2_clocks"
]



#tm = time.time()
#start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-180))
#end = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm))
#start= '2019-02-05T21:45:51'
#end= '2019-02-05T21:50:51'
#start= '2019-02-05T23:15:18'
#end= '2019-02-05T23:15:25'

gettimecmnd = 'ls -rt /home/ts8prod/jobHarness/jh_stage/LCA-11021_RTM/%s/*/connectivity0_2/v0/*/2*.log | tail -1 | xargs -n 1 grep "Starting power ON" | head -1 | awk -F "," \'{print $1}\'' % 'LCA-11021_RTM-004'
rawstart = os.popen(gettimecmnd).readline()
tm = time.mktime(time.strptime(rawstart.strip(),'%Y-%m-%d %H:%M:%S'))
start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-500))
end = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm+300))

print "start=",start
print "end=",end

#    ristart = time.strptime(rstart.strip(),'%Y-%m-%d %H:%M:%S')
#    ristop = time.strptime(rstop.strip(),'%Y-%m-%d %H:%M:%S')

#    tm = time.mktime(ristop)
#    start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-300))
#    end = time.strftime('%Y-%m-%dT%H:%M:%S',ristop)
    
#    milestones = ('2017-10-06T00:00:00', '2017-10-06T23:59:59')
    
    
if True :
    ccs_subsystem = 'ts8-otm1'
    
    config_file = 'ts8power_quantities.cfg'
    
    time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=600)
    config = ccs_trending.ccs_trending_config(config_file)
    for section in config.sections():
        print "doing section ",section
        plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                               time_axis=time_axis)
        plotter.read_config(config, section)
        title = "%s, %s, %s" % (test_id, run_number, section)
        plotter.plot(title=title)
#        os.mkdir('out_%s' % test_id)
        plt.savefig('out_%s_%s_%s_%s.png' % (test_id, section, test_id, run_number))
        plotter.save_file('out_%s_%s_%s_%s.txt' % (test_id, section, test_id, run_number))


print
print " ----------------------------------------------------------------------------------------"
print



