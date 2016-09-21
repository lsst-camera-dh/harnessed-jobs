set term png
set output 'pdvals.png'
set title "PhotoDiode Current Plot\nvs. time"
set xlabel "Time"
set ylabel "Current\nA"
set grid
set style data linespoints
set key left
plot pdfile using 1:2
#plot '/home/ts3prod/jobHarness/jh_stage/e2v-CCD/E2V-CCD250-049/preflight_acq/v0/14129/pd-values_1452134074-for-seq-3-exp-1.txt' using 1:2
replot
