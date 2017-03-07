###############################################################################
# fe55
# Acquire fe55 image pairs
#
###############################################################################

def WriteBiasVolt(fp,arcsub,valname):

    result = arcsub.synchCommand(10,"getLabeled",valname);
    vval = result.getResult();
    fp.write("%s|%s\n" % (valname,vval));

def WriteConstant(fp,arcsub,valname):

    result = arcsub.synchCommand(10,"getConstant",valname);
    vval = result.getResult();
    fp.write("%s|%s\n" % (valname,vval));

from org.lsst.ccs.scripting import *
from java.lang import Exception
import sys
import time
import eolib

CCS.setThrowExceptions(True);

try:
    #attach CCS subsystem Devices for scripting
    print "Attaching teststand subsystems"
    tssub  = CCS.attachSubsystem("%s" % ts);
    print "attaching Bias subsystem"
    biassub   = CCS.attachSubsystem("%s/Bias" % ts);
    print "attaching PD subsystem"
    pdsub   = CCS.attachSubsystem("%s/PhotoDiode" % ts);
#    print "attaching XED subsystem"
#    xedsub   = CCS.attachSubsystem("%s/Fe55" % ts);
    print "attaching Mono subsystem"
    monosub = CCS.attachSubsystem("%s/Monochromator" % ts );
    print "attaching PDU subsystem"
    pdusub = CCS.attachSubsystem("%s/PDU" % ts );
    print "Attaching archon subsystem"
    arcsub  = CCS.attachSubsystem("%s" % archon);
    
    time.sleep(3.)

    cdir = tsCWD

    
    ts_version = ""
    archon_version = ""
    ts_revision = ""
    archon_revision = ""

    ts_version,archon_version,ts_revision,archon_revision = eolib.EOgetCCSVersions(tssub,cdir)
except:
    print "pre-setup problem!"

eolib.EOSetup(tssub,CCDID,CCSCCDTYPE,cdir,acffile,vac_outlet,arcsub)


if (1==1) :
    fp = open("%s/bias-voltages.out" % (cdir),"w");
    
    istate=0;
    WriteConstant(fp,arcsub,"P_SLEW");
    WriteConstant(fp,arcsub,"S_SLEW");
    WriteConstant(fp,arcsub,"CL_LOW");
    WriteConstant(fp,arcsub,"CL_HIGH");
    WriteConstant(fp,arcsub,"ADCLAMP");
    WriteConstant(fp,arcsub,"T_LOW");
    WriteConstant(fp,arcsub,"T_HIGH");
    WriteConstant(fp,arcsub,"RG_SLEW");
    WriteConstant(fp,arcsub,"CL_SLEW");
    WriteConstant(fp,arcsub,"P_LOW");
    WriteConstant(fp,arcsub,"P_HIGH");
    WriteConstant(fp,arcsub,"S_LOW");
    WriteConstant(fp,arcsub,"S_HIGH");
    WriteConstant(fp,arcsub,"RG_LOW");
    WriteConstant(fp,arcsub,"RG_HIGH");

    WriteBiasVolt(fp,arcsub,"DD_V");
    WriteBiasVolt(fp,arcsub,"OD7_D1_V");
    WriteBiasVolt(fp,arcsub,"OD12_B2_V");
    WriteBiasVolt(fp,arcsub,"OD14_B3_V");
    WriteBiasVolt(fp,arcsub,"OD16_B4_V");
    WriteBiasVolt(fp,arcsub,"DD_V");
    WriteBiasVolt(fp,arcsub,"OD5_D2_V");
    WriteBiasVolt(fp,arcsub,"RD_V");
    WriteBiasVolt(fp,arcsub,"OD15_A4_V");
    WriteBiasVolt(fp,arcsub,"OD13_A3_V");
    WriteBiasVolt(fp,arcsub,"OD11_A2_V");
    WriteBiasVolt(fp,arcsub,"OD9_A1_V");
    WriteBiasVolt(fp,arcsub,"OD3_D3_V");
    WriteBiasVolt(fp,arcsub,"OD1_D4_V");
    WriteBiasVolt(fp,arcsub,"OD8_C1_V");
    WriteBiasVolt(fp,arcsub,"OD6_C2_V");
    WriteBiasVolt(fp,arcsub,"OD4_C3_V");
    WriteBiasVolt(fp,arcsub,"OD2_C4_V");
    WriteBiasVolt(fp,arcsub,"OD10_B1_V");
    WriteBiasVolt(fp,arcsub,"OD1_V");
    WriteBiasVolt(fp,arcsub,"OD10_V");
    WriteBiasVolt(fp,arcsub,"OD10_B1_V");
    WriteBiasVolt(fp,arcsub,"OD11_V");
    WriteBiasVolt(fp,arcsub,"OD11_A2_V");
    WriteBiasVolt(fp,arcsub,"OD12_V");
    WriteBiasVolt(fp,arcsub,"OD12_B2_V");
    WriteBiasVolt(fp,arcsub,"OD13_V");
    WriteBiasVolt(fp,arcsub,"OD13_A3_V");
    WriteBiasVolt(fp,arcsub,"OD14_V");
    WriteBiasVolt(fp,arcsub,"OD14_B3_V");
    WriteBiasVolt(fp,arcsub,"OD15_V");
    WriteBiasVolt(fp,arcsub,"OD15_A4_V");
    WriteBiasVolt(fp,arcsub,"OD16_V");
    WriteBiasVolt(fp,arcsub,"OD16_B4_V");
    WriteBiasVolt(fp,arcsub,"OD1_D4_V");
    WriteBiasVolt(fp,arcsub,"OD2_V");
    WriteBiasVolt(fp,arcsub,"OD2_C4_V");
    WriteBiasVolt(fp,arcsub,"OD3_V");
    WriteBiasVolt(fp,arcsub,"OD3_D3_V");
    WriteBiasVolt(fp,arcsub,"OD4_V");
    WriteBiasVolt(fp,arcsub,"OD4_C3_V");
    WriteBiasVolt(fp,arcsub,"OD5_V");
    WriteBiasVolt(fp,arcsub,"OD5_D2_V");
    WriteBiasVolt(fp,arcsub,"OD6_V");
    WriteBiasVolt(fp,arcsub,"OD6_C2_V");
    WriteBiasVolt(fp,arcsub,"OD7_V");
    WriteBiasVolt(fp,arcsub,"OD7_D1_V");
    WriteBiasVolt(fp,arcsub,"OD8_V");
    WriteBiasVolt(fp,arcsub,"OD8_C1_V");
    WriteBiasVolt(fp,arcsub,"OD9_V");
    WriteBiasVolt(fp,arcsub,"OD9_A1_V");
    WriteBiasVolt(fp,arcsub,"ODB_V");
    WriteBiasVolt(fp,arcsub,"ODT_V");
    WriteBiasVolt(fp,arcsub,"OG_V");
    WriteBiasVolt(fp,arcsub,"RD_V");
    WriteBiasVolt(fp,arcsub,"RDB_V");
    WriteBiasVolt(fp,arcsub,"RDT_V");
    WriteBiasVolt(fp,arcsub,"RG_V");
    WriteBiasVolt(fp,arcsub,"RGB_V");
    WriteBiasVolt(fp,arcsub,"RGT_V");
    WriteBiasVolt(fp,arcsub,"A1B_V");
    WriteBiasVolt(fp,arcsub,"A1T_V");
    WriteBiasVolt(fp,arcsub,"A2B_V");
    WriteBiasVolt(fp,arcsub,"A2T_V");
    WriteBiasVolt(fp,arcsub,"A3B_V");
    WriteBiasVolt(fp,arcsub,"A3T_V");
    WriteBiasVolt(fp,arcsub,"BB_V");
    WriteBiasVolt(fp,arcsub,"CLBAR_V");
    WriteBiasVolt(fp,arcsub,"DIO1_V");
    WriteBiasVolt(fp,arcsub,"DRV1_V");
    WriteBiasVolt(fp,arcsub,"DRV2_V");
    WriteBiasVolt(fp,arcsub,"DRV3_V");
    WriteBiasVolt(fp,arcsub,"DRV4_V");
    WriteBiasVolt(fp,arcsub,"HV1_V");
    WriteBiasVolt(fp,arcsub,"HV2_V");
    WriteBiasVolt(fp,arcsub,"HV3_V");
    WriteBiasVolt(fp,arcsub,"HV4_V");
    WriteBiasVolt(fp,arcsub,"N5VB_V");
    WriteBiasVolt(fp,arcsub,"N5VT_V");
    WriteBiasVolt(fp,arcsub,"N7V5A_V");
    WriteBiasVolt(fp,arcsub,"N7V5B_V");
    WriteBiasVolt(fp,arcsub,"OTG_V");
    WriteBiasVolt(fp,arcsub,"P1_V");
    WriteBiasVolt(fp,arcsub,"P2_V");
    WriteBiasVolt(fp,arcsub,"P3_V");
    WriteBiasVolt(fp,arcsub,"P4_V");
    WriteBiasVolt(fp,arcsub,"P5VB_V");
    WriteBiasVolt(fp,arcsub,"P5VT_V");
    WriteBiasVolt(fp,arcsub,"P7V5A_V");
    WriteBiasVolt(fp,arcsub,"P7V5B_V");
    WriteBiasVolt(fp,arcsub,"S1_V");
    WriteBiasVolt(fp,arcsub,"S1B_V");
    WriteBiasVolt(fp,arcsub,"S1T_V");
    WriteBiasVolt(fp,arcsub,"S2_V");
    WriteBiasVolt(fp,arcsub,"S2B_V");
    WriteBiasVolt(fp,arcsub,"S2T_V");
    WriteBiasVolt(fp,arcsub,"S3_V");
    WriteBiasVolt(fp,arcsub,"S3B_V");
    WriteBiasVolt(fp,arcsub,"S3T_V");
    WriteBiasVolt(fp,arcsub,"SC_V");
    WriteBiasVolt(fp,arcsub,"VBB_V");
    fp.close();

try:

    print "set controller parameters for an exposure with the shutter closed"
    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","Fe55","0");

#    arcsub.synchCommand(10,"setDefaultCCDTypeName","BNLITL");

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");

    print "Now collect some parameters from the config file"
    bcount = float(eolib.getCfgVal(acqcfgfile, 'FE55_BCOUNT', default = "2"))
    dcount = float(eolib.getCfgVal(acqcfgfile, 'FE55_DCOUNT', default = "2"))

    seq = 0

#number of PLCs between readings
    nplc = 1

    ccd = CCDID
    print "Working on CCD %s" % ccd

# clear the buffers
    print "doing some unrecorded bias acquisitions to clear the buffers"
    print "set controller for bias exposure"
    arcsub.synchCommand(10,"setParameter","Light","0");
    arcsub.synchCommand(10,"setParameter","ExpTime","0");
    for i in range(5):
        timestamp = time.time()
        result = arcsub.synchCommand(10,"setFitsFilename","");
        print "Ready to take clearing bias image. time = %f" % time.time()
        result = arcsub.synchCommand(20,"exposeAcquireAndSave");
        rply = result.getResult()
        result = arcsub.synchCommand(500,"waitForExpoEnd");
        rply = result.getResult();

# go through config file looking for 'fe55' instructions, take the fe55s
    print "Scanning config file for fe55 specifications";
    
    fp = open(acqcfgfile,"r");
    fpfiles = open("%s/acqfilelist" % cdir,"w");
    
    for line in fp:
        tokens = str.split(line)
        if ((len(tokens) > 0) and (tokens[0] == 'fe55')):
            exptime  = float(tokens[1])
            imcount = int(tokens[2])
    
            print "setting location of fits exposure directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));
    
# take bias images
            print "set controller for bias exposure"
            arcsub.synchCommand(10,"setParameter","Fe55","0");
            arcsub.synchCommand(10,"setParameter","Light","0");
            arcsub.synchCommand(10,"setParameter","ExpTime","0");
 
            print "setting location of bias fits directory"
            arcsub.synchCommand(10,"setFitsDirectory","%s" % (cdir));

            print "start bias exposure loop"

            for i in range(bcount):
                timestamp = time.time()

                print "set fits filename"
                fitsfilename = "%s_fe55_bias_%3.3d_${TIMESTAMP}.fits" % (ccd,i)
                result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
                result = arcsub.synchCommand(10,"setHeader","TestType","FE55")
                result = arcsub.synchCommand(10,"setHeader","ImageType","BIAS")

                print "Ready to take bias image. time = %f" % time.time()
                result = arcsub.synchCommand(20,"exposeAcquireAndSave");
                print "wait"
                fitsfilename = result.getResult();
                print "after click click at %f" % time.time()
                time.sleep(0.2)

            print "start fe55 exposures"
            arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
            nreads = exptime*60/nplc + 200
            if (nreads > 3000):
                nreads = 3000
                nplc = exptime*60/(nreads-200)
                print "Nreads limited to 3000. nplc set to %f to cover full exposure period " % nplc

            icount = 0
            for itype in range(2):
                if (itype==0) : 
                    itypename = "bias"
                    icount = dcount
                    arcsub.synchCommand(10,"setParameter","Fe55","0");
                if (itype==1) :
                    itypename = "fe55"
                    icount = imcount
                    arcsub.synchCommand(10,"setParameter","Fe55","1");

                print "Throwing away the first image"
                arcsub.synchCommand(10,"setFitsFilename","");
# set exposure time just before taking image
                arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));
                result = arcsub.synchCommand(200,"exposeAcquireAndSave");
                reply = result.getResult();

                time.sleep(2.0)

                result = arcsub.synchCommand(10,"setHeader","TestType","FE55")
                result = arcsub.synchCommand(10,"setHeader","ImageType","FE55")

                for i in range(icount):

#4ik
                    print "setting Nexpo back to single shot"
                    arcsub.synchCommand(10,"setParameter Nexpo 1");
                    print "picture taken"
# prepare to readout diodes                                                                              
# adjust timeout because we will be waiting for the data to become ready
                    mywait = nplc/60.*nreads*1.10 ;
                    print "Setting timeout to %f s" % mywait
                    pdsub.synchCommand(1000,"setTimeout",mywait);

                    pdresult =  pdsub.asynchCommand("accumBuffer",int(nreads),float(nplc),True);
#                pdresult =  pdsub.synchCommand(10,"accumBuffer",int(nreads),float(nplc),False);
                    print "recording should now be in progress and the time is %f" % time.time()
# start acquisition

                    timestamp = time.time()
    
# make sure to get some readings before the state of the shutter changes       
                    time.sleep(0.2);

# start acquisition
                    fitsfilename = "%s_fe55_%s_%3.3d_${TIMESTAMP}.fits" % (ccd,itypename,i+1)
                    result = arcsub.synchCommand(10,"setFitsFilename",fitsfilename);
    
                    print "Ready to take image. time = %f" % time.time()

# extend the Fe55 arm
#                print "extend the Fe55 arm"
#                xedsub.synchCommand(30,"extendFe55");
    

# set exposure time just before taking image
                    arcsub.synchCommand(10,"setParameter","ExpTime",str(int(exptime*1000)));

# take the image
                    fitsfilename = arcsub.synchCommand(200,"exposeAcquireAndSave").getResult();
                    rply = arcsub.synchCommand(500,"waitForExpoEnd").getResult();

# continuous unrecorded bias taking
                    arcsub.synchCommand(10,"setParameter","ExpTime","0");
                    arcsub.synchCommand(10,"setParameter Nexpo 100000");

# retract the Fe55 arm
#                xedsub.synchCommand(30,"retractFe55");
    
                    print "after click click at %f" % time.time()

                    print "done with exposure # %d" % i
                    print "getting photodiode readings at time = %f" % time.time();
    
                    pdfilename = "pd-values_%d-for-seq-%d-exp-%d.txt" % (timestamp,seq,i+1)
                    print "starting the wait for an accumBuffer done status message at %f" % time.time()
                    tottime = pdresult.get();

# make sure the sample of the photo diode is complete
                    time.sleep(5.)

                    print "executing readBuffer, cdir=%s , pdfilename = %s" % (cdir,pdfilename)
                    result = pdsub.synchCommand(500,"readBuffer","%s/%s" % (cdir,pdfilename));
                    buff = result.getResult()
                    print "Finished getting readings at %f" % time.time()
    
                    result = arcsub.synchCommand(200,"addBinaryTable","%s/%s" % (cdir,pdfilename),fitsfilename,"AMP0.MEAS_TIMES","AMP0_MEAS_TIMES","AMP0_A_CURRENT",timestamp)
                    fpfiles.write("%s %s/%s %f\n" % (fitsfilename,cdir,pdfilename,timestamp))
    
                seq = seq + 1
    
    fpfiles.close();
    fp.close();
    
    
    fp = open("%s/status.out" % (cdir),"w");
    
    istate=0;
    result = tssub.synchCommandLine(10,"getstate");
    istate=result.getResult();
    fp.write(`istate`+"\n");
    fp.write("%s\n" % ts_version);
    fp.write("%s\n" % ts_revision);
    fp.write("%s\n" % archon_version);
    fp.write("%s\n" % archon_revision);
    fp.close();
    
# move TS to idle state
    result = tssub.synchCommand(200,"setTSReady");
    rply = result.getResult();

# get the glowing vacuum gauge back on
    result = pdusub.synchCommand(120,"setOutletState",vac_outlet,True);
    rply = result.getResult();

    time.sleep(5.)

    result = pdsub.synchCommand(10,"softReset");
    buff = result.getResult()

    arcsub.synchCommand(10,"setParameter","Fe55","0");

    result = arcsub.synchCommand(10,"setHeader","TestType","FE55-DONE")

except Exception, ex:                                                     

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");
    
    arcsub.synchCommand(10,"setParameter","Fe55","0");

    raise Exception("There was an exception in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

    result = arcsub.synchCommand(10,"setHeader","TestType","FE55-ERR")

#except ScriptingTimeoutException, ex:                                                     

# retract the Fe55 arm
#    xedsub.synchCommand(30,"retractFe55");
    
#    arcsub.synchCommand(10,"setParameter","Fe55","0");

#    raise Exception("There was an ScriptingTimeoutException in the acquisition producer script. The message is\n (%s)\nPlease retry the step or contact an expert," % ex)

print "FE55: END"
