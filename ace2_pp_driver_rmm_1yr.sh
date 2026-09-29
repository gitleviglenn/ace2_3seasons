#!/usr/bin/env bash

wkdir='/home/C823281551/code/pythonCode/ACE2'
cd $wkdir

echo 'working directory is: '
echo $wkdir

seas=("2005" "2013" "2024")

echo 'hold on, this takes a while...'
ensnum=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10")
decnum=("dec01" "dec02" "dec03" "dec04")
for bacon in ${seas[@]}; do
    for french in ${decnum[@]}; do
        for toast in ${ensnum[@]}; do
    	echo 'just a little bit more'
    	echo ${french} 'not your fault' ${toast}
            python find_rmm_1yr.py nan ${bacon} ${french} ${toast} 
        done
    done 
done
#python find_rmm_1yr.py nan 2013 dec04 10 99
