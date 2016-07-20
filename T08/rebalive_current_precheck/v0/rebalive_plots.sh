#!/bin/tcsh
#foreach i (ts8/DR00.Reb2.Temp1 ts8/DR00.Reb2.Temp2 ts8/R00.Reb2.Temp1 ts8/R00.Reb2.Temp2 ts8/R00.Reb2.Temp3 ts8/R00.Reb2.Temp4 ts8/R00.Reb2.Temp5 ts8/R00.Reb2.Temp6 ts8/R00.Reb2.Temp7 ts8/R00.Reb2.Temp8 ts8/DR00.Reb2.6Vv ts8/DR00.Reb2.6Vi ts8/DR00.Reb2.9Vv ts8/DR00.Reb2.9Vi ts8/DR00.Reb2.24Vv ts8/DR00.Reb2.24Vi ts8/DR00.Reb2.40Vv ts8/DR00.Reb2.40Vi ts8/DR00.Reb1.Temp1 ts8/DR00.Reb1.Temp2 ts8/R00.Reb1.Temp1 ts8/R00.Reb1.Temp2 ts8/R00.Reb1.Temp3 ts8/R00.Reb1.Temp4 ts8/R00.Reb1.Temp5 ts8/R00.Reb1.Temp6 ts8/R00.Reb1.Temp7 ts8/R00.Reb1.Temp8 ts8/DR00.Reb1.6Vv ts8/DR00.Reb1.6Vi ts8/DR00.Reb1.9Vv ts8/DR00.Reb1.9Vi ts8/DR00.Reb1.24Vv ts8/DR00.Reb1.24Vi ts8/DR00.Reb1.40Vv ts8/DR00.Reb1.40Vi ts8/DR00.Reb0.Temp1 ts8/DR00.Reb0.Temp2 ts8/R00.Reb0.Temp1 ts8/R00.Reb0.Temp2 ts8/R00.Reb0.Temp3 ts8/R00.Reb0.Temp4 ts8/R00.Reb0.Temp5 ts8/R00.Reb0.Temp6 ts8/R00.Reb0.Temp7 ts8/R00.Reb0.Temp8 ts8/DR00.Reb0.6Vv ts8/DR00.Reb0.6Vi ts8/DR00.Reb0.9Vv ts8/DR00.Reb0.9Vi ts8/DR00.Reb0.24Vv ts8/DR00.Reb0.24Vi ts8/DR00.Reb0.40Vv ts8/DR00.Reb0.40Vi ccs-rebps/RebPsState/mainPowerState ccs-rebps/RebPsState/powerState ccs-rebps/RebPsState/hvBiasDacs ccs-rebps/RebPsState/psId)
foreach i (`cat plotchans.list`)
echo "generate plot data for $i"
#set selection = 'select FROM_UNIXTIME(tstampmills/1000.),doubleData from rawdata where descr_id in (select id from datadesc where name='\"$i\"') order by -tstampmills limit 300;'
set selection = 'select id from datadesc where name='\"$i\"';'
echo "selection=("$selection")"

set getid = 'mysql CCSTrending4 -h lsstdb2.rcf.bnl.gov -u ccs -s -r --password=vst4lsst --execute='\'"$selection"\'''
echo getid = $getid
#eval $getid
set id = `eval $getid | tail -1`
echo id for $i is $id

#set selection = 'select tstampmills/1000.,doubleData from rawdata where descr_id in (select id from datadesc where name='\"$i\"') order by -tstampmills limit 300;'
set selection = 'select tstampmills/1000.,doubleData from rawdata where descr_id='$id' order by -tstampmills limit 300;'
echo "selection=("$selection")"
set outfl = `echo $i | awk -F '/' '{print $2}'`
echo "title time "$i >! $outfl.dat
eval mysql CCSTrending4 -h lsstdb2.rcf.bnl.gov -u ccs -s -r --password=vst4lsst --execute=\'$selection\'  >> $outfl.dat
end

foreach i (`ls -1 *.dat | awk -F "." '{print $1"."$2"."substr($3,1,1) }' | sort -u`)

echo "joining files of prefix $i"

rm data.dat
touch data.dat

foreach j (`ls -1 $i*.dat`)
echo "joining file $j"
join -a 2 data.dat $j | sed 's/ time / /' > data2.dat
mv data2.dat data.dat
end

eval gnuplot rebalive_plots.gp
mv data.dat $i-joined.dat
eval mv plot.png $i.png
end
