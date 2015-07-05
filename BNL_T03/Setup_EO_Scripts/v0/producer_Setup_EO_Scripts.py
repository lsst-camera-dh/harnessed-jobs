#!/usr/bin/env python
import os
import sys
import subprocess


tag = os.environ["EO_SCRIPTS_TAG"]
tag = os.environ["EO_SCRIPTS_HOME"]


print "The realease of harnessed-jobs with tag %s will be installed" % tag
 
os.system("cd %s ; wget https://github.com/lsst-camera-dh/harnessed-jobs/archive/%s.tar.gz ." % (eohome,tag))
os.system("cd %s ; tar -vzxf %s.tar.gz" % (eohome,tag))
os.system("cd %s ; mv harnessed-jobs old-harnessed-jobs-`date +%R-%f`" % eohome)
os.system("cd %s ; ln -s harnessed-jobs-%s harnessed-jobs" % (eohome,tag))

print "The release has been installed."
