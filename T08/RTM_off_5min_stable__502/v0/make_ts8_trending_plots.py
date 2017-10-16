import matplotlib.pyplot as plt
import ccs_trending
import siteUtils
import time

raft_id = getLSSTId()
run_number = getRunNumber()
host = 'localhost'
ccs_subsystem = 'ts'

#start = '2017-10-06T00:00:00'                                                                        
#end = '2017-10-13T18:19:22'                                                                           
tm = time.time()
start = ctime(tm-300)
end = ctime(tm)

milestones = ('2017-10-06T00:00:00', '2017-10-06T23:59:59')

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
