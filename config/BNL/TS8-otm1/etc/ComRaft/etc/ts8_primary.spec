# Specification file for primary header. Taken from LCA 10140 v1
#
MONDIODE    Float   ${ts/photodiodecurrent}     Current in the monitoring diode (nA)
CCDBSS      Float   ${MeasuredCCDBSS}           CCD bias voltage
FILTER      String  ${ts/TSState/filter}        Name of the filter
FILTPOS     Integer ${ts/filter1position}       Filter position
CCDGAIN     Float   1.00                        Rough guess at overall system gain (e-/DNB)
CCDNOISE    Float   0                           Rough guess at system noise (e- rms)
PIXRATE     Float   ${PixelReadRate}            Rate for pixel reads
SEQNUM      Integer ${TS8GlobalKeywords.SequenceNumber} Sequence number extracted from the original filename
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
#HIERARCH.AMP2-ON         Integer ${ts/TSState/biasstate}      If voltage source is switched on
HIERARCH.AMP2-VOLTAGE    Float   ${ts/ccdbiasvoltage}         [V] voltage level
HIERARCH.AMP2-CURRENT    Float   ${ts/TSState/picocurrent}    [pA] measured current (in picoAmps)
HIERARCH.AMP2-ZERO_CHECK String  off                          Zero check on/off
