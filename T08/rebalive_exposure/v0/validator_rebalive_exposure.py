#!/usr/bin/env python
from ccsTools import ccsValidator
import os
import siteUtils
import shutil
import lcatr.schema
import glob
import pyfits
import sys
import numpy
import numpy.random
import Tkinter

jobDir = siteUtils.getJobDir()

shutil.copy("%s/rebalive_plots.gp" % jobDir ,os.getcwd())
shutil.copy("%s/rebalive_plots.sh" % jobDir ,os.getcwd())
shutil.copy("%s/plotchans.list" % jobDir ,os.getcwd())

#os.system("./rebalive_plots.sh 2>&1 logpl")

jobName = "rebalive_exposure"


# open images in rebalive_exposure, check for response to light
# POC 20170316

#import /astro/u/poc1/TS8_Commissioning/Python/boxes.py


def boxesmean(d, BOXSZ=100, NUMBOXES=500, ximg=[10,522], yimg=[1,2002]):
    """ compute mean of 500 ROI and return median -- for avoiding cosmics, defects etc """
    yo = numpy.random.randint(yimg[0], yimg[1], NUMBOXES)
    xo = numpy.random.randint(ximg[0], ximg[1], NUMBOXES)
    return  numpy.median([d[yo[i]:yo[i]+BOXSZ,xo[i]:xo[i]+BOXSZ].mean() for i in range(NUMBOXES)])


YIMG = [10,1990]  # rows in image and overscan areas
XIMG = [10,500]   # columns in image areas
OIMG = [515,570]  # columns in overscan areas

# connectivity test image filenames used
fl0=sorted(glob.glob('*alive_test*fits'))
fl1=sorted(glob.glob('*1000ms*fits'))
fl4=sorted(glob.glob('*4000ms*fits'))

# make list of slots, segments, and amps
slots = []
for f in fl0:
    slots.append([f[:2]] * 16)
slots = slots[0] + slots[1] + slots[2] + slots[3] + slots[4] + slots[5] + slots[6] + slots[7] + slots[8]
#slots = slots[0] + slots[1] + slots[2]
#slots = sum(slots)

segments = ['10','11','12','13','14','15','16','17','07','06','05','04','03','02','01','00'] * 9

amps = range(1,17)*9
#print "fl0=",fl0

i0 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl0 for i in range(1,17)])

o0 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl0 for i in range(1,17)])

sig0 = i0 - o0

i1 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl1 for i in range(1,17)])

o1 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl1 for i in range(1,17)])

sig1 = i1 - o1

i4 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl4 for i in range(1,17)])

o4 = numpy.array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl4 for i in range(1,17)])

sig4 = i4 - o4

# now search for non-responsive channels
bad0 = numpy.where(sig0 < numpy.median(sig0)/10.)[0]
bad1 = numpy.where(sig1 < numpy.median(sig1)/10.)[0]
bad4 = numpy.where(sig4 < numpy.median(sig4)/10.)[0]

print("0 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad0], sig0[bad0])
print("1 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad1], sig1[bad1])
print("4 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad4], sig4[bad4])

ofile = open('/tmp/conntest', 'w')
print >> ofile, ("0 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad0], sig0[bad0])
print >> ofile, ("1 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad1], sig1[bad1])
print >> ofile, ("4 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad4], sig4[bad4])
ofile.close()

os.system('cat /tmp/conntest >> rebalive_results_exposures.txt')


if (not "ready" in jobDir) :
    for i in range(2):
         print "This image viewing may be skipped. Skip the step (N/y)?"
    sys.stdout.flush()
    answer = raw_input("\n\nThis image viewing may be skipped. Skip the step (N/y)? \n\n")
    if "y" in answer.lower() :
         print "Operator requested to skip the step. BYE"
    else :
    
    
        apptxt = "Please check the image that is about to be projected in ds9"
        
        print apptxt
        topq = Tkinter.Tk()
        q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
        q.pack()
        topq.title('FLAT image check')
        topq.mainloop()
        
        qefiles = sorted(glob.glob('*flat*.fits'))
        if len(qefiles)>0 :
             os.system("ds9 -mosaicimage iraf -scale datasec no -zscale -lock frame image *flat*fits")
        






for i in range(2) :
     print "RETEST (N/y)?"
sys.stdout.flush()
answer = raw_input("RETEST (N/y)?")
if "y" in answer.lower() :
     raise Exception("PURPOSELY crashing to allow a retest via retrying the e-Traveler step")



results = []

alivefiles = glob.glob("*.txt")
alivefiles = alivefiles + glob.glob("*summary*")
alivefiles = alivefiles + glob.glob("*png")
alivefiles = alivefiles + glob.glob("*log*")
alivefiles = alivefiles + glob.glob("*fits")

data_products = [lcatr.schema.fileref.make(item) for item in alivefiles]
results.extend(data_products)

statusAssignments = {}

schemaFile = open("%s/%s_runtime.schema.new"%(jobDir,jobName),"w")
schemaFile.write("# -*- python -*-\n")
schemaFile.write("{\n")
schemaFile.write("    \'schema_name\' : \'%s_runtime\',\n"%jobName)
schemaFile.write("    \'schema_version\' : 0,\n")

statusFile = open("rebalive_results_exposures.txt")
lnum = 0
for line in statusFile:
#    print "line = %s" % line

#    line = line.replace('OK','<font color="green">OK</font>').replace('FAILED','<font color="red">FAILED</font>')

    key = "line%03d" % lnum
    statusAssignments[key] = "%s" % line
    schemaFile.write("    \'%s\' : str,\n" % key)

    lnum = lnum + 1

while (lnum<240):
    key = "line%03d" % lnum
    statusAssignments[key] = "blank"
    schemaFile.write("    \'%s\' : str,\n"%key)

    lnum = lnum + 1


schemaFile.write("}\n")
schemaFile.close()

print "statusAssignments = %s" % statusAssignments

print "jobName = %s" % jobName
lcatr.schema.load("%s/%s_runtime.schema"%(jobDir,jobName))
print "schema = %s" % str(lcatr.schema.get("%s_runtime"%jobName))

#results.append(lcatr.schema.valid(lcatr.schema.get(jobName),
#                                      **statusAssignments))
results.append(lcatr.schema.valid(lcatr.schema.get("%s_runtime"%jobName),
                                      **statusAssignments))

#results.append(siteUtils.packageVersions())

lcatr.schema.write_file(results)
lcatr.schema.validate_file()


#ccsValidator('rebalive_exposure')
