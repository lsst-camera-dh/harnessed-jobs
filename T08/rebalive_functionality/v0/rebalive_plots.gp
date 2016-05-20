set term png
set key autotitle columnhead
set output 'plot.png'
set xlabel "Date\nTime"
set timefmt "%Y-%m-%d %H:%M:%S"
set xdata time
set format x "%d/%m\n%H:%M"
set grid
set key left
plot 'data.dat' using 1:3
replot
