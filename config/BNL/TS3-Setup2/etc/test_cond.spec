# Specification file for tset_cond header. Taken from LCA 10140 v1
#
EXTNAME     String  "TEST_COND"                 Name of the extension
TEMP_SET    Float   ${ts2/ccdtempsetpoint}       Temperature set point
CCDTEMP     Float   ${ts2/ccdtemperature}        Measured temperature
ROOMTEMP    Float   ${ts2/roomtemperature}       Room Temperature
DWRTEMP	    Float   ${ts2/ccdtemperature}        External Dewar Temperature
DWRPRESS    Float   ${ts2/dewarpressure}         Dewar internal pressure level
SRCTYPE     String  ${ts2/TSState/srctype}       Type of light source used
SRCMODL     String  ${ts2/TSState/srctype}       Manufacturer’s Model number
SRCPWR      Float   ${ts2/lamppower}             Light source power
ND_FILT     Integer ${ts2/TSState/fltpos}        ND Filter after lamp (if any)
FILTER      String  ${ts2/TSState/filter}        Optical Filter used
MONOTYPE    String  ${ts2/TSState/monotype}	
MONOMODL    String  ${ts2/TSState/monotype}      Monochromator model number
MONOPOS     Integer ${ts2/monochromgrating}      Monochromator grating turret position
MONOGRAT    Integer ${ts2/monochromgrating}      Monochromator grating in use
MONOWL      Float   ${MonochromaterWavelength}  Monochromator WL setting
PD_MODEL    String  ${ts2/TSState/pdtype}        Monitor Photodiode model number
PD_SER      String  ${PhotodiodeSignal}         Monitor Photodiode serial number
