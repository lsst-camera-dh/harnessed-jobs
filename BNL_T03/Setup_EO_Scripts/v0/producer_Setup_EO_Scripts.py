#!/usr/bin/env python
import os
import sys
import subprocess


tag = os.environ["EO_SCRIPTS_TAG"]
eohome = os.environ["EO_SCRIPTS_HOME"]


print "The release of harnessed-jobs with tag %s will be installed" % tag
cwd = os.getcwd() 
print "copying old installation of harnessed jobs to a safe place"
os.system("cd %s ; cp -Lrvp harnessed-jobs old-harnessed-jobs-`date +%%F-%%R`" % eohome)
print "moving the original to /tmp"
os.system("cd %s ; cp -Lvrp harnessed-jobs /tmp/ ; mv harnessed-jobs moved-harnessed-jobs" % eohome)
print "downloading tar of new tag"
os.system("cd %s ; wget https://github.com/lsst-camera-dh/harnessed-jobs/archive/%s.tar.gz" % (eohome,tag))
print "untarring"
os.system("cd %s ; tar -vzxf %s.tar.gz" % (eohome,tag))
print "making a link to it"
os.system("cd %s ; ln -s harnessed-jobs-%s harnessed-jobs" % (eohome,tag))

os.system("cd %s" % cwd)

print "The release has been installed."
