#!/bin/tcsh
foreach i (ts8/DR00.Reb2.Temp1 ts8/DR00.Reb2.Temp2 ts8/R00.Reb2.Temp1 ts8/R00.Reb2.Temp2 ts8/R00.Reb2.Temp3 ts8/R00.Reb2.Temp4 ts8/R00.Reb2.Temp5 ts8/R00.Reb2.Temp6 ts8/R00.Reb2.Temp7 ts8/R00.Reb2.Temp8 ts8/DR00.Reb2.6Vv ts8/DR00.Reb2.6Vi ts8/DR00.Reb2.9Vv ts8/DR00.Reb2.9Vi ts8/DR00.Reb2.24Vv ts8/DR00.Reb2.24Vi ts8/DR00.Reb2.40Vv ts8/DR00.Reb2.40Vi ts8/DR00.Reb1.Temp1 ts8/DR00.Reb1.Temp2 ts8/R00.Reb1.Temp1 ts8/R00.Reb1.Temp2 ts8/R00.Reb1.Temp3 ts8/R00.Reb1.Temp4 ts8/R00.Reb1.Temp5 ts8/R00.Reb1.Temp6 ts8/R00.Reb1.Temp7 ts8/R00.Reb1.Temp8 ts8/DR00.Reb1.6Vv ts8/DR00.Reb1.6Vi ts8/DR00.Reb1.9Vv ts8/DR00.Reb1.9Vi ts8/DR00.Reb1.24Vv ts8/DR00.Reb1.24Vi ts8/DR00.Reb1.40Vv ts8/DR00.Reb1.40Vi ts8/DR00.Reb0.Temp1 ts8/DR00.Reb0.Temp2 ts8/R00.Reb0.Temp1 ts8/R00.Reb0.Temp2 ts8/R00.Reb0.Temp3 ts8/R00.Reb0.Temp4 ts8/R00.Reb0.Temp5 ts8/R00.Reb0.Temp6 ts8/R00.Reb0.Temp7 ts8/R00.Reb0.Temp8 ts8/DR00.Reb0.6Vv ts8/DR00.Reb0.6Vi ts8/DR00.Reb0.9Vv ts8/DR00.Reb0.9Vi ts8/DR00.Reb0.24Vv ts8/DR00.Reb0.24Vi ts8/DR00.Reb0.40Vv ts8/DR00.Reb0.40Vi ccs-rebps/RebPsState/mainPowerState ccs-rebps/RebPsState/powerState ccs-rebps/RebPsState/hvBiasDacs ccs-rebps/RebPsState/psId)
echo "generate plot data for $i"
set selection = 'select FROM_UNIXTIME(tstampmills/1000.),doubleData from rawdata where descr_id in (select id from datadesc where name='\"$i\"') order by -tstampmills limit 300;'
echo "selection=("$selection")"
echo "title time "$i >! data.dat
eval mysql CCSTrending4 -h lsstdb2.rcf.bnl.gov -u ccs -s -r --password=vst4lsst --execute=\'$selection\'  >> data.dat
eval gnuplot rebalive_plots.gp
set outfl = `echo $i | awk -F '/' '{print $2}'`
eval mv plot.png $outfl.png
end
