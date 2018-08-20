# Specification file for tset_cond header. Taken from LCA 10140 v1
#
EXTNAME     String  "TEST_COND"                 Name of the extension
TEMP_SET    Float   ${ts/ccdtempsetpoint}       Temperature set point
CCDTEMP     Float   ${ts/ccdtemperature}        Measured temperature
ROOMTEMP    Float   ${ts/roomtemperature}       Room Temperature
DWRTEMP	    Float   ${ts/ccdtemperature}        External Dewar Temperature
DWRPRESS    Float   ${ts/dewarpressure}         Dewar internal pressure level
SRCTYPE     String  ${ts/TSState/srctype}       Type of light source used
SRCMODL     String  ${ts/TSState/srctype}       Manufacturer’s Model number
SRCPWR      Float   ${ts/lamppower}             Light source power
ND_FILT     Integer ${ts/TSState/fltpos}        ND Filter after lamp (if any)
FILTER      String  ${ts/TSState/filter}        Optical Filter used
MONOTYPE    String  ${ts/TSState/monotype}	
MONOMODL    String  ${ts/TSState/monotype}      Monochromator model number
MONOPOS     Integer ${ts/monochromgrating}      Monochromator grating turret position
MONOGRAT    Integer ${ts/monochromgrating}      Monochromator grating in use
MONOWL      Float   ${MonochromaterWavelength}  Monochromator WL setting
PD_MODEL    String  ${ts/TSState/pdtype}        Monitor Photodiode model number
PD_SER      String  ${PhotodiodeSignal}         Monitor Photodiode serial number
