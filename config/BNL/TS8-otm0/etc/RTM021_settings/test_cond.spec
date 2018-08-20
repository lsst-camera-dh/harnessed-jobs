# Specification file for tset_cond header. Taken from LCA 10140 v1
#
EXTNAME     String  "TEST_COND"                 Name of the extension
TEMP_SET    Float   ${StatusAggregator.ts/ccdtempsetpoint}       Temperature set point
SENSTEMP    Float   ${MeasuredTemperature}             Measured sensor temperature
ROOMTEMP    Float   ${StatusAggregator.ts/roomtemperature}       Room Temperature
CRYOTEMP    Float   ${StatusAggregator.ts/temp_c}                Cryo Plate Temperature
COLDTEMP    Float   ${StatusAggregator.ts/temp_b}                Cold Plate Temperature
DWRPRESS    Float   ${StatusAggregator.ts/dewarpressure}         Dewar internal pressure level
SRCTYPE     String  ${StatusAggregator.ts/TSState/srctype}       Type of light source used
SRCMODL     String  ${StatusAggregator.ts/TSState/srctype}       Manufacturer’s Model number
SRCPWR      Float   ${StatusAggregator.ts/lamppower}             Light source power
ND_FILT     Integer ${StatusAggregator.ts/TSState/fltpos}        ND Filter after lamp (if any)
FILTER      String  ${StatusAggregator.ts/TSState/filter}        Optical Filter used
MONOTYPE    String  ${StatusAggregator.ts/TSState/monotype}	
MONOMODL    String  ${StatusAggregator.ts/TSState/monotype}      Monochromator model number
MONOPOS     Integer ${StatusAggregator.ts/monochromgrating}      Monochromator grating turret position
MONOGRAT    Integer ${StatusAggregator.ts/monochromgrating}      Monochromator grating in use
MONOWL      Float   ${MonochromatorWavelength}  Monochromator WL setting
PD_MODEL    String  ${StatusAggregator.ts/TSState/pdtype}        Monitor Photodiode model number
PD_SER      String  ${PhotodiodeSignal}         Monitor Photodiode serial number
