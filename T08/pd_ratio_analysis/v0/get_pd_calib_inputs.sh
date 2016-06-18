#!/bin/bash
#Example:
#[jh-test ts8prod@ts8-raft1 mr]$ ./get_pd_calib_inputs.sh /home/ts8prod/jobHarness/jh_stage/ITL-CCD/TS8-PD-RATIO-TST2/mono_calib_acq/v0/ 283284
#export pdir=~/jobHarness/jh_stage/BNL_Test_Stand/TS3-2/mono_calib_acq/v0/
#export job_id=17926
export pdir=$1
export job_id=$2
export ts=`date +%Y%m%d%H%M`

cd $pdir

pwd

ls -1 $job_id/pdbias-*.txt | xargs -n 1 awk '{if ($2<-1.e-11) {nval++;sumv+=$2} else {nbase++;sumb+=$2}} END{"grep "FILENAME" $job_id/acqfilelist" | getline ffln;if (nval>0) print substr(ffln,index(ffln,"lambda")+7,5),(sumv/nval-sumb/nbase)}' | sort -k 1b,1 | sed 's/_//g' > ~/PD_RATIO-$ts-pd2.txt

ls -1 $job_id/pd-*.txt | xargs -n 1 awk '{if ($2<-1.e-9) {nval++;sumv+=$2} else {nbase++;sumb+=$2}} END{"grep "FILENAME" $job_id/acqfilelist" | getline ffln;if (nval>0) print substr(ffln,index(ffln,"lambda")+7,5),(sumv/nval-sumb/nbase)}' | sort -k 1b,1 | sed 's/_//g' > ~/PD_RATIO-$ts-pd1.txt

join ~/PD_RATIO-$ts-pd1.txt ~/PD_RATIO-$ts-pd2.txt | sort -n | awk '{print $1/10.","$2","$3","$2/$3}' > PD_RATIO-$ts-EOT-Mono-Calib.csv


cd ~/mr/

cp $pdir/PD_RATIO-$ts-EOT-Mono-Calib.csv .
./make_ratio_file.py PD_RATIO-$ts-EOT-Mono-Calib.csv pd_ratio_$ts-PD_RATIO-3J019.txt --pd_area .6361e-4 --pd_sens_file 3j019.csv
