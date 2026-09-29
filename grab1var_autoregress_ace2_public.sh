#!/usr/bin/env bash

# grabs just one variable from the autoregressive_predictions file to reduce size of 
# files we want to work with.  

wkdir='/data/ACE2'
cd $wkdir

echo 'working directory is: '
echo $wkdir

# this is Juhyun's directory
origFiledir='/ACE2_share/ACE2_simulation_output/'

# The lines below extract the precipitation variable from the larger autoregressive_predictions file that is very large..
tcSeasons=("2005" "2013" "2024")
decade=("dec01" "dec02" "dec03" "dec04")
for i in ${tcSeasons[@]}; do 
  for j in ${decade[@]}; do
    echo 'do you need to grab only precip and rewrite the precip data to decades? '
    ls -l ${origFiledir}'/'${i}/${j}/autoregressive_predictions.nc
#    ncks -v PRATEsfc ${origFiledir}'/'${i}/${j}/autoregressive_predictions.nc -O 'autoregressive_predictions_'${i}'_'${j}'_PRATEsfc.nc'
    ncks -v total_water_path ${origFiledir}'/'${i}/${j}/autoregressive_predictions.nc -O 'autoregressive_predictions_'${i}'_'${j}'_TWP.nc'
  done
done

