set term png
#set key autotitle columnhead
set xlabel "Date\nTime"
#set timefmt "%Y-%m-%d %H:%M:%S"
set timefmt "%s"
set xdata time
set format x "%d/%m\n%H:%M"
set grid
set key left

set output 'BoardTemp.png'
plot 'BoardTemp.dat' using 1:2 with lines
replot

set output 'R00.Reb0.Temp.png'
plot 'R00.Reb0.Temp1.dat' using 1:2 with lines, 'R00.Reb0.Temp2.dat' using 1:2 with lines, 'R00.Reb0.Temp3.dat' using 1:2 with lines, 'R00.Reb0.Temp4.dat' using 1:2 with lines, 'R00.Reb0.Temp5.dat' using 1:2 with lines, 'R00.Reb0.Temp6.dat' using 1:2 with lines, 'R00.Reb0.Temp7.dat' using 1:2 with lines, 'R00.Reb0.Temp8.dat' using 1:2 with lines, 'DR00.Reb0.Temp1.dat' using 1:2 with lines, 'DR00.Reb0.Temp2.dat' using 1:2 with lines
replot

set output 'R00.Reb1.Temp.png'
plot 'R00.Reb1.Temp1.dat' using 1:2 with lines, 'R00.Reb1.Temp2.dat' using 1:2 with lines, 'R00.Reb1.Temp3.dat' using 1:2 with lines, 'R00.Reb1.Temp4.dat' using 1:2 with lines, 'R00.Reb1.Temp5.dat' using 1:2 with lines, 'R00.Reb1.Temp6.dat' using 1:2 with lines, 'R00.Reb1.Temp7.dat' using 1:2 with lines, 'R00.Reb1.Temp8.dat' using 1:2 with lines, 'DR00.Reb1.Temp1.dat' using 1:2 with lines, 'DR00.Reb1.Temp2.dat' using 1:2 with lines
replot
