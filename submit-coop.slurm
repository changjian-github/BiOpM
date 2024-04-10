#!/bin/sh
#SBATCH --mail-user=cmjdxy@foxmail.com
#SBATCH --mail-type=all
#SBATCH --array=0-79
#SBATCH --job-name=coop
#SBATCH --partition=std
#SBATCH --time=120:00:00
#SBATCH -o logs/output/coop-%a.o
#SBATCH -e logs/error/coop-%a.e

cd $SLURM_SUBMIT_DIR

case $SLURM_ARRAY_TASK_ID in
     0) ARG="--para pmed17-p25,8,10-800-1,0";;
     1) ARG="--para pmed20-p50,8,10-800-1,0";;
     2) ARG="--para pmed22-p62,8,10-800-1,0";;
     3) ARG="--para pmed28-p75,8,10-800-1,0";;
     4) ARG="--para pmed33-p87,8,10-800-1,0";;
     5) ARG="--para pmed36-p100,8,10-800-1,0";;
     6) ARG="--para pmed39-p112,8,10-800-1,0";;
     7) ARG="--para pmed40-p225,8,10-800-1,0";;
     8) ARG="--para pmed17-p25,8,10-800-1,1";;
     9) ARG="--para pmed20-p50,8,10-800-1,1";;
    10) ARG="--para pmed22-p62,8,10-800-1,1";;
    11) ARG="--para pmed28-p75,8,10-800-1,1";;
    12) ARG="--para pmed33-p87,8,10-800-1,1";;
    13) ARG="--para pmed36-p100,8,10-800-1,1";;
    14) ARG="--para pmed39-p112,8,10-800-1,1";;
    15) ARG="--para pmed40-p225,8,10-800-1,1";;
    16) ARG="--para pmed17-p25,8,10-800-1,2";;
    17) ARG="--para pmed20-p50,8,10-800-1,2";;
    18) ARG="--para pmed22-p62,8,10-800-1,2";;
    19) ARG="--para pmed28-p75,8,10-800-1,2";;
    20) ARG="--para pmed33-p87,8,10-800-1,2";;
    21) ARG="--para pmed36-p100,8,10-800-1,2";;
    22) ARG="--para pmed39-p112,8,10-800-1,2";;
    23) ARG="--para pmed40-p225,8,10-800-1,2";;
    24) ARG="--para pmed17-p25,8,10-800-1,3";;
    25) ARG="--para pmed20-p50,8,10-800-1,3";;
    26) ARG="--para pmed22-p62,8,10-800-1,3";;
    27) ARG="--para pmed28-p75,8,10-800-1,3";;
    28) ARG="--para pmed33-p87,8,10-800-1,3";;
    29) ARG="--para pmed36-p100,8,10-800-1,3";;
    30) ARG="--para pmed39-p112,8,10-800-1,3";;
    31) ARG="--para pmed40-p225,8,10-800-1,3";;
    32) ARG="--para pmed17-p25,8,10-800-1,4";;
    33) ARG="--para pmed20-p50,8,10-800-1,4";;
    34) ARG="--para pmed22-p62,8,10-800-1,4";;
    35) ARG="--para pmed28-p75,8,10-800-1,4";;
    36) ARG="--para pmed33-p87,8,10-800-1,4";;
    37) ARG="--para pmed36-p100,8,10-800-1,4";;
    38) ARG="--para pmed39-p112,8,10-800-1,4";;
    39) ARG="--para pmed40-p225,8,10-800-1,4";;
    40) ARG="--para pmed17-p25,8,10-800-1,5";;
    41) ARG="--para pmed20-p50,8,10-800-1,5";;
    42) ARG="--para pmed22-p62,8,10-800-1,5";;
    43) ARG="--para pmed28-p75,8,10-800-1,5";;
    44) ARG="--para pmed33-p87,8,10-800-1,5";;
    45) ARG="--para pmed36-p100,8,10-800-1,5";;
    46) ARG="--para pmed39-p112,8,10-800-1,5";;
    47) ARG="--para pmed40-p225,8,10-800-1,5";;
    48) ARG="--para pmed17-p25,8,10-800-1,6";;
    49) ARG="--para pmed20-p50,8,10-800-1,6";;
    50) ARG="--para pmed22-p62,8,10-800-1,6";;
    51) ARG="--para pmed28-p75,8,10-800-1,6";;
    52) ARG="--para pmed33-p87,8,10-800-1,6";;
    53) ARG="--para pmed36-p100,8,10-800-1,6";;
    54) ARG="--para pmed39-p112,8,10-800-1,6";;
    55) ARG="--para pmed40-p225,8,10-800-1,6";;
    56) ARG="--para pmed17-p25,8,10-800-1,7";;
    57) ARG="--para pmed20-p50,8,10-800-1,7";;
    58) ARG="--para pmed22-p62,8,10-800-1,7";;
    59) ARG="--para pmed28-p75,8,10-800-1,7";;
    60) ARG="--para pmed33-p87,8,10-800-1,7";;
    61) ARG="--para pmed36-p100,8,10-800-1,7";;
    62) ARG="--para pmed39-p112,8,10-800-1,7";;
    63) ARG="--para pmed40-p225,8,10-800-1,7";;
    64) ARG="--para pmed17-p25,8,10-800-1,8";;
    65) ARG="--para pmed20-p50,8,10-800-1,8";;
    66) ARG="--para pmed22-p62,8,10-800-1,8";;
    67) ARG="--para pmed28-p75,8,10-800-1,8";;
    68) ARG="--para pmed33-p87,8,10-800-1,8";;
    69) ARG="--para pmed36-p100,8,10-800-1,8";;
    70) ARG="--para pmed39-p112,8,10-800-1,8";;
    71) ARG="--para pmed40-p225,8,10-800-1,8";;
    72) ARG="--para pmed17-p25,8,10-800-1,9";;
    73) ARG="--para pmed20-p50,8,10-800-1,9";;
    74) ARG="--para pmed22-p62,8,10-800-1,9";;
    75) ARG="--para pmed28-p75,8,10-800-1,9";;
    76) ARG="--para pmed33-p87,8,10-800-1,9";;
    77) ARG="--para pmed36-p100,8,10-800-1,9";;
    78) ARG="--para pmed39-p112,8,10-800-1,9";;
    79) ARG="--para pmed40-p225,8,10-800-1,9";;
esac

python xlab_coop.py $ARG
