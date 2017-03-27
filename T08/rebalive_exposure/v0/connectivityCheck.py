# /usr/bin/python
# open images in rebalive_exposure, check for response to light
# POC 20170316

import pyfits, glob
#import /astro/u/poc1/TS8_Commissioning/Python/boxes.py


def boxesmean(d, BOXSZ=100, NUMBOXES=500, ximg=[10,522], yimg=[1,2002]):
    """ compute mean of 500 ROI and return median -- for avoiding cosmics, defects etc """
    yo = randint(yimg[0], yimg[1], NUMBOXES)
    xo = randint(ximg[0], ximg[1], NUMBOXES)
    return  median([d[yo[i]:yo[i]+BOXSZ,xo[i]:xo[i]+BOXSZ].mean() for i in range(NUMBOXES)])


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

segments = ['10','11','12','13','14','15','16','17','07','06','05','04','03','02','01','00'] * 9

amps = range(1,17)*9

i0 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl0 for i in range(1,17)])

o0 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl0 for i in range(1,17)])

sig0 = i0 - o0

i1 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl1 for i in range(1,17)])

o1 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl1 for i in range(1,17)])

sig1 = i1 - o1

i4 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=XIMG) for f in fl4 for i in range(1,17)])

o4 = array([boxesmean(pyfits.getdata(f,i), BOXSZ=10, NUMBOXES=50, yimg=YIMG, ximg=OIMG) for f in fl4 for i in range(1,17)])

sig4 = i4 - o4

# now search for non-responsive channels
bad0 = find(sig0 < median(sig0)/10.)
bad1 = find(sig1 < median(sig1)/10.)
bad4 = find(sig4 < median(sig4)/10.)

print("0 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad0], sig0[bad0])
print("1 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad1], sig1[bad1])
print("4 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad4], sig4[bad4])

ofile = open('/tmp/conntest', 'w')
print >> ofile, ("0 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad0], sig0[bad0])
print >> ofile, ("1 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad1], sig1[bad1])
print >> ofile, ("4 sec: (bad slot,bad segment, bad amp), signal " , [(slots[x],segments[x],amps[x])  for x in bad4], sig4[bad4])
ofile.close()
