#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import shutil
import os
import matplotlib.pyplot as plt
import ccs_trending
import siteUtils
import time

jobDir = siteUtils.getJobDir()

shutil.copy("%s/ts_quantities.cfg" % jobDir ,os.getcwd())
shutil.copy("%s/ts8_quantities.cfg" % jobDir ,os.getcwd())

ccsProducer('RTM_thermo', 'ccsthermal.py')
#ccsProducer('RTM_thermo', 'ts7_stats.py')


raft_id = siteUtils.getLSSTId()
run_number = siteUtils.getRunNumber()
host = 'localhost'
ccs_subsystem = 'ts'

tm = time.time()
start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-300))
end = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm))

milestones = ('2017-10-06T00:00:00', '2017-10-06T23:59:59')

config_file = 'ts_quantities.cfg'

time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1000)
config = ccs_trending.ccs_trending_config(config_file)
for section in config.sections():
    plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                           time_axis=time_axis)
    plotter.read_config(config, section)
    title = "%s, %s, %s" % (raft_id, run_number, section)
    plotter.plot(title=title)
    plt.savefig('%s_%s_%s.png' % (section, raft_id, run_number))
    plotter.save_file('%s_%s_%s.txt' % (section, raft_id, run_number))




ccs_subsystem = 'ts8'

config_file = 'ts8_quantities.cfg'

time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1000)
config = ccs_trending.ccs_trending_config(config_file)
for section in config.sections():
    plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                           time_axis=time_axis)
    plotter.read_config(config, section)
    title = "%s, %s, %s" % (raft_id, run_number, section)
    plotter.plot(title=title)
    plt.savefig('%s_%s_%s.png' % (section, raft_id, run_number))
    plotter.save_file('%s_%s_%s.txt' % (section, raft_id, run_number))


