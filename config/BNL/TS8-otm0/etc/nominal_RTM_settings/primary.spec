# Specification file for primary header. Taken from LCA 10140 v1
#
ORIGIN      String  ${Origin}                   Which site acquired the data
DATE        Date    ${FileCreationTime}         Creation Date and Time of File
DATE-OBS    Date    ${ObservationDate}          Date of the observation (image acquisition), UTC
MJD         MJD     ${FileCreationTime}         Modified Julian Date that the file was written
MJD-OBS     MJD     ${ObservationDate}          Modified Julian Date (5 decimal places) of image acquisition
RUNNUM      String  ${RunNumber}                The Run Number
IMAGETAG    String  ${Tag}                      Image tag (CCS/VST)
TSTAND      String  ${TestStand}                Which Test stand at the site was used
INSTRUME    String  ${Instrument}               CCD Controller type
CONTROLL    String  ${Instrument}               Duplicates INSTRUME
CONTNUM     Integer ${CCDControllerSerial}      CCD Controller Serial Number
SEQFILE     String  ${SequencerFileName}        Name of Sequencer File
CCD_MANU    String  ${CCDManufacturer}          CCD Manufacturer
CCD_TYPE    String  ${CCDModel}                 CCD Model Number
CCD_SERN    String  ${CCDSerialManufacturer}    Manufacturers’ CCD Serial Number
LSST_NUM    String  ${CCDSerialLSST}            LSST Assigned CCD Number
RAFTNAME    String  ${RaftName}                 Name of the RTM
REBNAME     String  ${RebName}                  Name of the REB
TESTTYPE    String  ${TestType}                 DARK:FLAT:OBS:PPUMP:QE:SFLAT
IMGTYPE     String  ${ImageType}                BIAS, DARK, …
SEQNUM      Integer ${SequenceNumber}           Sequence number extracted from the original filename
DETSIZE     String  ${DETSIZE}
TEMP_SET    Float   ${TemperatureSetPoint}      Temperature set point (deg C)
CCDTEMP     Float   ${MeasuredTemperature}      Measured temperature (deg C)
MONOWL      Float   ${MonochromatorWavelength}  Monochromator wavelength (nm)
FILTER      String  ${FilterName}               Name of the filter
EXPTIME     Float   ${ExposureTime}             Exposure Time in Seconds
SHUT_DEL    Float   ${ShutterDelay}             Delay between shutter close command and readout (msec)
FILENAME    String  ${OriginalFileName}         Original name of the file
BINX        Integer 1                           [pixels] binning along X axis 
BINY        Integer 1                           [pixels] binning along Y axis 
HEADVER     Integer 1                           Version number of header
CCDGAIN     Float   5.52                        Rough guess at overall system gain (e-/DNB)
CCDNOISE    Float   6                           Rough guess at system noise (e- rms)
