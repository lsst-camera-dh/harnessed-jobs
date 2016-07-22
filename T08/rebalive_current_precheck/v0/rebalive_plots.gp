set term png
#set key autotitle columnhead
set xlabel "Date\nTime"
#set timefmt "%Y-%m-%d %H:%M:%S"
set timefmt "%s"
set xdata time
set format x "%d/%m\n%H:%M"
set grid
set key left

set output 'R00.Reb2.AnaV.png'
plot 'R00.Reb2.AnaV.dat' using 1:2 with lines
replot

set output 'R00.Reb2.CCDI00.png'
plot 'R00.Reb2.CCDI000.dat' using 1:2 with lines, 'R00.Reb2.CCDI001.dat' using 1:2 with lines, 'R00.Reb2.CCDI002.dat' using 1:2 with lines, 'R00.Reb2.CCDI003.dat' using 1:2 with lines, 'R00.Reb2.CCDI004.dat' using 1:2 with lines, 'R00.Reb2.CCDI005.dat' using 1:2 with lines, 'R00.Reb2.CCDI006.dat' using 1:2 with lines, 'R00.Reb2.CCDI007.dat' using 1:2 with lines
replot

set output 'R00.Reb2.CCDI01.png'
plot 'R00.Reb2.CCDI010.dat' using 1:2 with lines, 'R00.Reb2.CCDI011.dat' using 1:2 with lines, 'R00.Reb2.CCDI012.dat' using 1:2 with lines, 'R00.Reb2.CCDI013.dat' using 1:2 with lines, 'R00.Reb2.CCDI014.dat' using 1:2 with lines, 'R00.Reb2.CCDI015.dat' using 1:2 with lines, 'R00.Reb2.CCDI016.dat' using 1:2 with lines, 'R00.Reb2.CCDI017.dat' using 1:2 with lines
replot


set output 'R00.Reb2.CCDI10.png'
plot 'R00.Reb2.CCDI100.dat' using 1:2 with lines, 'R00.Reb2.CCDI101.dat' using 1:2 with lines, 'R00.Reb2.CCDI102.dat' using 1:2 with lines, 'R00.Reb2.CCDI103.dat' using 1:2 with lines, 'R00.Reb2.CCDI104.dat' using 1:2 with lines, 'R00.Reb2.CCDI105.dat' using 1:2 with lines, 'R00.Reb2.CCDI106.dat' using 1:2 with lines, 'R00.Reb2.CCDI107.dat' using 1:2 with lines
replot

set output 'R00.Reb2.CCDI11.png'
plot 'R00.Reb2.CCDI110.dat' using 1:2 with lines, 'R00.Reb2.CCDI111.dat' using 1:2 with lines, 'R00.Reb2.CCDI112.dat' using 1:2 with lines, 'R00.Reb2.CCDI113.dat' using 1:2 with lines, 'R00.Reb2.CCDI114.dat' using 1:2 with lines, 'R00.Reb2.CCDI115.dat' using 1:2 with lines, 'R00.Reb2.CCDI116.dat' using 1:2 with lines, 'R00.Reb2.CCDI117.dat' using 1:2 with lines
replot

set output 'R00.Reb2.CCDI20.png'
plot 'R00.Reb2.CCDI200.dat' using 1:2 with lines, 'R00.Reb2.CCDI201.dat' using 1:2 with lines, 'R00.Reb2.CCDI202.dat' using 1:2 with lines, 'R00.Reb2.CCDI203.dat' using 1:2 with lines, 'R00.Reb2.CCDI204.dat' using 1:2 with lines, 'R00.Reb2.CCDI205.dat' using 1:2 with lines, 'R00.Reb2.CCDI206.dat' using 1:2 with lines, 'R00.Reb2.CCDI207.dat' using 1:2 with lines
replot

set output 'R00.Reb2.CCDI21.png'
plot 'R00.Reb2.CCDI210.dat' using 1:2 with lines, 'R00.Reb2.CCDI211.dat' using 1:2 with lines, 'R00.Reb2.CCDI212.dat' using 1:2 with lines, 'R00.Reb2.CCDI213.dat' using 1:2 with lines, 'R00.Reb2.CCDI214.dat' using 1:2 with lines, 'R00.Reb2.CCDI215.dat' using 1:2 with lines, 'R00.Reb2.CCDI216.dat' using 1:2 with lines, 'R00.Reb2.CCDI217.dat' using 1:2 with lines
replot

set output 'R00.Reb2.ClkI.png'
plot 'R00.Reb2.ClkI.dat' using 1:2 with lines
replot

set output 'R00.Reb2.ClkV.png'
plot 'R00.Reb2.ClkV.dat' using 1:2 with lines
replot

set output 'R00.Reb2.DigI.png'
plot 'R00.Reb2.DigI.dat' using 1:2 with lines
replot

set output 'R00.Reb2.DigV.png'
plot 'R00.Reb2.DigV.dat' using 1:2 with lines
replot


set output 'R00.Reb2.GD.png'
plot 'R00.Reb2.GD0V.dat' using 1:2 with lines, 'R00.Reb2.GD1V.dat' using 1:2 with lines, 'R00.Reb2.GD2V.dat' using 1:2 with lines
replot

set output 'ODV.png'
plot 'R00.Reb2.OD0V.dat' using 1:2 with lines, 'R00.Reb2.OD1V.dat' using 1:2 with lines, 'R00.Reb2.OD2V.dat' using 1:2 with lines, 'R00.Reb2.ODV.dat' using 1:2 with lines, 'REB0.OD.VaftLDO2.dat' using 1:2 with lines, 'REB0.OD.VaftLDO.dat' using 1:2 with lines, 'REB0.OD.VaftSwch.dat' using 1:2 with lines, 'REB0.OD.VbefLDO.dat' using 1:2 with lines
replot

set output 'ODI.png'
plot 'R00.Reb2.ODI.dat' using 1:2 with lines, 'REB0.OD.IaftLDO.dat' using 1:2 with lines, 'REB0.OD.IbefLDO.dat' using 1:2 with lines
replot

set output 'OGV.png'
plot 'R00.Reb2.OG0V.dat' using 1:2 with lines, 'R00.Reb2.OG1V.dat' using 1:2 with lines, 'R00.Reb2.OG2V.dat' using 1:2 with lines
replot

set output 'RDV.png'
plot 'R00.Reb2.RD0V.dat' using 1:2 with lines, 'R00.Reb2.RD1V.dat' using 1:2 with lines, 'R00.Reb2.RD2V.dat' using 1:2 with lines
replot

set output 'refV.png'
plot 'R00.Reb2.Ref05V.dat' using 1:2 with lines, 'R00.Reb2.Ref125V.dat' using 1:2 with lines, 'R00.Reb2.Ref15V.dat' using 1:2 with lines, 'R00.Reb2.Ref25V.dat' using 1:2 with lines
replot

# ---------------------------------------------------------------------------------------------------------------------------------
set output 'REB0-Iaftbef.png'
plot 'REB0.analog.IaftLDO.dat' using 1:2 with lines, 'REB0.analog.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-Vaftbef.png'
plot 'REB0.analog.VaftLDO.dat' using 1:2 with lines, 'REB0.analog.VaftSwch.dat' using 1:2 with lines, 'REB0.analog.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-clockV.png'
plot 'REB0.clockhi.VaftLDO.dat' using 1:2 with lines, 'REB0.clockhi.VaftSwch.dat' using 1:2 with lines, 'REB0.clockhi.VbefLDO.dat' using 1:2 with lines, 'REB0.clocklo.VaftLDO2.dat' using 1:2 with lines, 'REB0.clocklo.VaftLDO.dat' using 1:2 with lines, 'REB0.clocklo.VaftSwch.dat' using 1:2 with lines, 'REB0.clocklo.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-clockI.png'
plot 'REB0.clockhi.IaftLDO.dat' using 1:2 with lines, 'REB0.clockhi.IbefLDO.dat' using 1:2 with lines, 'REB0.clocklo.IaftLDO.dat' using 1:2 with lines, 'REB0.clocklo.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-digI.png'
plot 'REB0.digital.IaftLDO.dat' using 1:2 with lines, 'REB0.digital.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-digV.png'
plot 'REB0.digital.VaftLDO.dat' using 1:2 with lines, 'REB0.digital.VaftSwch.dat' using 1:2 with lines, 'REB0.digital.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-heaterI.png'
plot 'REB0.heater.IaftLDO.dat' using 1:2 with lines, 'REB0.heater.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-heaterV.png'
plot 'REB0.heater.VaftLDO.dat' using 1:2 with lines, 'REB0.heater.VaftSwch.dat' using 1:2 with lines, 'REB0.heater.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB0-hvbiasI.png'
plot 'REB0.hvbias.IbefSwch.dat' using 1:2 with lines
replot

set output 'REB0-hvbiasV.png'
plot 'REB0.hvbias.VbefSwch.dat' using 1:2 with lines
replot
# ---------------------------------------------------------------------------------------------------------------------------------
set output 'REB1-Iaftbef.png'
plot 'REB1.analog.IaftLDO.dat' using 1:2 with lines, 'REB1.analog.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-Vaftbef.png'
plot 'REB1.analog.VaftLDO.dat' using 1:2 with lines, 'REB1.analog.VaftSwch.dat' using 1:2 with lines, 'REB1.analog.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-clockV.png'
plot 'REB1.clockhi.VaftLDO.dat' using 1:2 with lines, 'REB1.clockhi.VaftSwch.dat' using 1:2 with lines, 'REB1.clockhi.VbefLDO.dat' using 1:2 with lines, 'REB1.clocklo.VaftLDO2.dat' using 1:2 with lines, 'REB1.clocklo.VaftLDO.dat' using 1:2 with lines, 'REB1.clocklo.VaftSwch.dat' using 1:2 with lines, 'REB1.clocklo.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-clockI.png'
plot 'REB1.clockhi.IaftLDO.dat' using 1:2 with lines, 'REB1.clockhi.IbefLDO.dat' using 1:2 with lines, 'REB1.clocklo.IaftLDO.dat' using 1:2 with lines, 'REB1.clocklo.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-digI.png'
plot 'REB1.digital.IaftLDO.dat' using 1:2 with lines, 'REB1.digital.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-digV.png'
plot 'REB1.digital.VaftLDO.dat' using 1:2 with lines, 'REB1.digital.VaftSwch.dat' using 1:2 with lines, 'REB1.digital.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-heaterI.png'
plot 'REB1.heater.IaftLDO.dat' using 1:2 with lines, 'REB1.heater.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-heaterV.png'
plot 'REB1.heater.VaftLDO.dat' using 1:2 with lines, 'REB1.heater.VaftSwch.dat' using 1:2 with lines, 'REB1.heater.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB1-hvbiasI.png'
plot 'REB1.hvbias.IbefSwch.dat' using 1:2 with lines
replot

set output 'REB1-hvbiasV.png'
plot 'REB1.hvbias.VbefSwch.dat' using 1:2 with lines
replot
# ---------------------------------------------------------------------------------------------------------------------------------
set output 'REB2-Iaftbef.png'
plot 'REB2.analog.IaftLDO.dat' using 1:2 with lines, 'REB2.analog.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-Vaftbef.png'
plot 'REB2.analog.VaftLDO.dat' using 1:2 with lines, 'REB2.analog.VaftSwch.dat' using 1:2 with lines, 'REB2.analog.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-clockV.png'
plot 'REB2.clockhi.VaftLDO.dat' using 1:2 with lines, 'REB2.clockhi.VaftSwch.dat' using 1:2 with lines, 'REB2.clockhi.VbefLDO.dat' using 1:2 with lines, 'REB2.clocklo.VaftLDO2.dat' using 1:2 with lines, 'REB2.clocklo.VaftLDO.dat' using 1:2 with lines, 'REB2.clocklo.VaftSwch.dat' using 1:2 with lines, 'REB2.clocklo.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-clockI.png'
plot 'REB2.clockhi.IaftLDO.dat' using 1:2 with lines, 'REB2.clockhi.IbefLDO.dat' using 1:2 with lines, 'REB2.clocklo.IaftLDO.dat' using 1:2 with lines, 'REB2.clocklo.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-digI.png'
plot 'REB2.digital.IaftLDO.dat' using 1:2 with lines, 'REB2.digital.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-digV.png'
plot 'REB2.digital.VaftLDO.dat' using 1:2 with lines, 'REB2.digital.VaftSwch.dat' using 1:2 with lines, 'REB2.digital.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-heaterI.png'
plot 'REB2.heater.IaftLDO.dat' using 1:2 with lines, 'REB2.heater.IbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-heaterV.png'
plot 'REB2.heater.VaftLDO.dat' using 1:2 with lines, 'REB2.heater.VaftSwch.dat' using 1:2 with lines, 'REB2.heater.VbefLDO.dat' using 1:2 with lines
replot

set output 'REB2-hvbiasI.png'
plot 'REB2.hvbias.IbefSwch.dat' using 1:2 with lines
replot

set output 'REB2-hvbiasV.png'
plot 'REB2.hvbias.VbefSwch.dat' using 1:2 with lines
replot
