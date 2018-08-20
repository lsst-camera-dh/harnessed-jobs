#!/usr/bin/env python
from ccsTools import ccsProducer
import os
from eTraveler.clientAPI.connection import Connection
from lcatr.harness.et_wrapper import getHardwareHierarchy
import sys
import siteUtils

# Assume top-level directory is in an environment variable
#topdir = os.environ.get('DATADIR')
topdir = os.getcwd()
topparts = topdir.split('/')
activity_id = topparts[len(topparts)-1]
if not topdir:
    raise RuntimeError, 'cannot determine top-level data directory'

# Save list of subdirectories. Their names are the manufacturer id's
# of the components to be processed
#manIds = list(os.listdir(topdir))

# Connect to eTraveler (prod) server with intent to use Dev database
limsurl = ""
try:
    limsurl = os.environ['LCATR_LIMS_URL']
except :
    pass
if ('/Dev' in limsurl) :
    print "Connecting to eTraveler Dev"
    conn = Connection('homer', 'Dev', prodServer=True)
else :
    print "Connecting to eTraveler Prod"
    conn = Connection('homer', 'Prod', prodServer=True)


if not conn:
    raise RuntimeError, 'unable to authenticate'

rsp = []
try:
#    act = 23278
#    act = siteUtils.extractJobId(topdir)
    act = int(activity_id)
    print "Activity ID = %d" % act
    rsp = conn.getRunInfo(activityId=act)

    print('Results from getRunInfo for activity %d\n' % (act))
    for k in rsp:
        print ('For key %s returned value is %s\n' % (k, rsp[k]) )

#    sys.exit(0)
except Exception,msg:
    print 'Operation failed with exception: '
    print  msg
    sys.exit(1)


rsp = []
try:
#    rsp = conn.getHardwareHierarchy(experimentSN='LCA-10753_RSA-002_CTE_ETU',
#                                      htype='LCA-10753_RSA',
#                                      noBatched='false')
    rsp = conn.getHardwareHierarchy(experimentSN=siteUtils.getUnitId(),
                                      htype=siteUtils.getUnitType(),
                                      noBatched='false')
    print "Results from getHardwareHierarchy unfiltered:"
    iDict = 0
    for d in rsp:
        print('Examining array element %d' % (iDict))
        isaccd = False
        ccd_sn = ""
        ccd_slot = ""
        ccd_htype = ""
        got_manu_info = False
        for k in d:
            if "ccd" in k.lower() :
                print('For key {0} value is {1}'.format(k, d[k]))
                if ('child_hardwareTypeName value' in k and ('itl-ccd' in d[k].lower() or 'e2v-ccd' in d[k].lower()) ) :
                    isaccd = True
                if (isaccd and 'child_experimentSN' in str(k)) :
                    ccd_sn = str(d[k])
                if (isaccd and 'slotName' in str(k)) :
                    ccd_slot = str(d[k])
                if (isaccd and 'child_hardwareTypeName' in str(k)) :
                    ccd_htype = str(d[k])
                if (isaccd and ccd_sn != "" and ccd_htype != "" and not got_manu_info) :
                    print "trying to get Manufacturer ID for ccd_sn=%s , ccd_htype=%s" % (ccd_sn,ccd_htype)
                    try: 
                        rsp = conn.getManufacturerId(experimentSN=ccd_sn,
                                                       htype=ccd_htype)
                        print 'Manufacturer ID: ', rsp
                        got_manu_info = True
                    except ValueError,msg:
                        print 'Operation failed with ValueError: ', msg
                    except Exception,msg:
                        print 'Operation failed with exception: '
                        print  msg
                        sys.exit(1)
        iDict +=1
#    sys.exit(0)
except Exception,msg:
    print 'Operation failed with exception: '
    print  msg
    sys.exit(1)


#dictArray = conn.getHardwareHierarchy(noBatched='true')
#print dictArray

os.system('ts7VQMoff')
ccsProducer('eo_acq', 'ccseo.py')
os.system('ts7VQMon')

try:
    os.system("cp -p %s ." % sequence_file)
except:
    pass


#examining array element 15
#For key child_hardwareTypeName value is ITL-CCD
#For key parent_experimentSN value is LCA-10753_RSA-002_CTE_ETU
#For key level value is 0
#For key relationshipTypeName value is RSA_contains_ITL-CCDs
#For key child_experimentSN value is ITL-NULL5_CTE-ETU
#For key parent_hardwareTypeName value is LCA-10753_RSA
#For key parent_id value is 704
#For key child_id value is 756
#For key slotName value is S20
