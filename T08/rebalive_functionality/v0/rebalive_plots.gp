set term png
set key autotitle columnhead
set output 'plot.png'
set xlabel "Date\nTime"
#set timefmt "%Y-%m-%d %H:%M:%S"
#set xdata time
#set format x "%d/%m\n%H:%M"
set grid
set key left
#plot 'data.dat' using 1:3
#plot 'data.dat'
plot 'data.dat' using  1:2, '' using 1:3, '' using 1:4, '' using 1:5, '' using 1:6, '' using 1:7, '' using 1:8, '' using 1:9
replot
