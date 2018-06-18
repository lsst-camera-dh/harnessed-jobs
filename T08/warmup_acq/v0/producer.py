#!/usr/bin/env python
from ccsTools import ccsProducer
import Tkinter
import glob
import os
import sys
import time


doit = True

print "\n\nPress return to start the warm-up. The operator must return to acknowledge that it is OK to power off the PT-30 when the first temperature ramp of the cryo plate has ended. Enter \"n\" to skip. - "
sys.stdout.flush()
answer = raw_input("")

if not 'n' in answer:
     print "executing ccsrtmwarmup-step1.py"
     if (doit) :
          os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/RTM-warmup/v0/ccsrtmwarmup-step1.py")
#     ccsProducer('RTM_warmup', 'ccsrtmwarmup-step1.py')

#for i in range(20):
print "\n\nThe cryo plate temperature should now be above the that of the cold plates and it is OK to turn off the PT-30. Press return to have the PT-30 turned off and to proceed with the warming of the cryo plate to room temperature. Enter \"n\" to skip. - "
sys.stdout.flush()
answer = raw_input("")

if (doit) :
     os.system('ts7PT30off')

if not 'n' in answer:
     print "executing ccsrtmwarmup-step2.py"
     if (doit) :
          os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/RTM-warmup/v0/ccsrtmwarmup-step2.py")
#     ccsProducer('RTM_warmup', 'ccsrtmwarmup-step2.py')


if (True) :
    sys.stdout.flush()


#    apptxt = "NOTE: text boxes are currently not being used because it would me that the steps would need to be executed from the same desktop."

#    print apptxt
#    topq = Tkinter.Tk()
#    q = Tkinter.Button(topq, text = apptxt, command = topq.destroy, bg = "yellow", font = ("Helvetica",24))
#    q.pack()
#    topq.title('FLAT image check')
#    topq.mainloop()

 
#apptxt = "The job is finished."
#topd = Tkinter.Tk()
#d = Tkinter.Button(topd, text = apptxt, command = topd.destroy, bg = "yellow",# font = ("Helvetica",24))
#d.pack()
#topd.title('DONE')
#topd.mainloop()

print "\n\nThe cryo plate temperature should now be at or near room temperature and it is OK to turn off the NF-55s. Press return to turn off the REBs. Enter \"n\" to skip. - "
sys.stdout.flush()
answer = raw_input("")


if not 'n' in answer:
     
     print "turning off NF55 #1"
     sys.stdout.flush()

     if (doit) :
          os.system('ts7NF551off')
          time.sleep(120.0)

     print "turning off NF55 #2"
     sys.stdout.flush()

     if (doit) :
          os.system('ts7NF552off')
          time.sleep(120.0)

     print "executing ccsrtmwarmup-step3.py"
     if (doit) :
          os.system("$CCS_BIN_DIR/ScriptExecutor $VIRTUAL_ENV/share/RTM-warmup/v0/ccsrtmwarmup-step3.py")
#     ccsProducer('RTM_warmup', 'ccsrtmwarmup-step3.py')
