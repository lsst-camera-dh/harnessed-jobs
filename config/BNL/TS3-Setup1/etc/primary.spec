# Specification file for primary header. Taken from LCA 10140 v1
#
ORIGIN      String  ${Origin}                   Which site acquired the data
DATE        Date    ${FileCreationDate}         Creation Date and Time of File
DATE-OBS    Date    ${ObservationDate}          Date of the observation (image acquisition), UTC
MJD-OBS     MJD     ${ObservationDate}          Modified Julian Date of image acquisition
IMAGETAG    String  ${Tag}                      Image tag (CCS/VST)
TSTAND      String  ${TestStand}                Which Test stand at the site was used
INSTRUME    String  ${Instrument}               CCD Controller type
CONTROLL    String  ${Instrument}               Duplicates INSTRUME
CONTNUM     Integer ${CCDControllerSerial}      CCD Controller Serial Number
CCD_MANU    String  ${CCDManufacturer}          CCD Manufacturer
CCD_TYPE    String  ${CCDModel}                 CCD Model Number
CCD_SERN    String  ${CCDSerialManufacturer}    Manufacturers’ CCD Serial Number
LSST_NUM    String  ${CCDSerialManufacturer}    LSST Assigned CCD Number
TESTTYPE    String  ${TestType}                 DARK:FLAT:OBS:PPUMP:QE:SFLAT
IMGTYPE     String  ${ImageType}                BIAS, DARK, …
SEQNUM      Integer ${SequenceNumber}           Sequence number extracted from the original filename
TEMP_SET    Float   ${ts/ccdtempsetpoint}       Temperature set point (deg C)
CCDTEMP     Float   ${ts/ccdtemperature}        Measured temperature (deg C)
CCDBSS      Float   ${ts/ccdbiasvoltage}        CCD bias voltage
MONDIODE    Float   ${ts/photodiodecurrent}     Current in the monitoring diode (nA)
MONOWL      Float   ${MonochromatorWavelength}  Monochromator wavelength (nm)
PIXRATE     Float   ${PixelReadRate}            Rate for pixel reads
FILTER      String  ${ts/TSState/filter}        Name of the filter
FILTPOS     Integer ${ts/filter1position}       Filter position
EXPTIME     Float   ${ExposureTime}             Exposure Time in Seconds
SHUT_DEL    Float   ${ShutterDelay}             Delay between shutter close command and readout (msec)
CTLRCFG     String  ${ConfigFile}               Name of the CCD controller configuration file
FILENAME    String  ${OriginalFileName}         Original name of the file
DETSIZE     String  ${DETSIZE}                  NOAO MOSAIC keywords
BINX        Integer 1                           [pixels] binning along X axis 
BINY        Integer 1                           [pixels] binning along Y axis 
HEADVER     Integer 1                           Version number of header
CCDGAIN     Float   2.98                        Rough guess at overall system gain (e-/DNB)
CCDNOISE    Float   6                           Rough guess at system noise (e- rms)
CFGFILE     String  ${ConfigFile}               Configuration file name
HIERARCH.MONOCH-WAVELENG Float   ${ts/monochromatorwavelength} monochromator wavelength
HIERARCH.MONOCH-SLIT_A   Float   ${ts/monochromatorslit1}     Width of the A slit in um
HIERARCH.MONOCH-SLIT_B   Float   ${ts/monochromatorslit2}     Width of the B slit in um
HIERARCH.MONOCH-SLIT_C   Float   0                            Width of the C slit in um
HIERARCH.MONOCH-BANDPASS Float   ${ts/monochromband}          Automatic slit width in nm
HIERARCH.MONOCH-FILT_1   Float   ${ts/filter1position}        filter position
HIERARCH.MONOCH-MSTEPS   Float   ${ts/monochromstep}          Current grating position in terms of motor step
HIERARCH.MONOCH-GRATING  Float   ${ts/monochromgrating}       Grating position
HIERARCH.AMP0-IDN        String  ${ts/TSState/pdtype}         Monitor Photodiode model number
HIERARCH.AMP0-AZERO      String  F                            SYSTEM:AZERO value
HIERARCH.AMP0-COUNT      Integer ${ts/TSState/pdcnt}          number of measurements (buffer length)
HIERARCH.AMP0-MEAS_NPLC  Integer ${ts/TSState/pdnplc}         Time of each measurment. In Hz multiples (1 = 1
HIERARCH.AMP2-IDN        String  ${ts/TSState/biastype}       identification string
HIERARCH.AMP2-ON         Integer ${ts/TSState/biasstate}      If voltage source is switched on
HIERARCH.AMP2-VOLTAGE    Float   ${ts/ccdbiasvoltage}         [V] voltage level
HIERARCH.AMP2-CURRENT    Float   ${ts/TSState/picocurrent}    [pA] measured current (in picoAmps)
HIERARCH.AMP2-ZERO_CHECK String  off                          Zero check on/off
