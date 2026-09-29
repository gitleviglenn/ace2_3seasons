#!/usr/bin/env bash

# grabs just the precipitation from the very large autoregressive_predictions.nc files

# uses ncks to select the particular timesteps that correspond to 1 year chunks so that we can break
# files that contain 5 ensemble members into files containing only 1 ensemble member.

# this is a mess.       not proud to attach my name: levi silvers

wkdir='/data/ACE2'
cd $wkdir

echo 'working directory is: '
echo $wkdir

origFiledir='/ACE2_share/ACE2_simulation_output/'

tcSeason="2013"
#decnum="02"
#decnum=("01" "02" "03" "04")
decnum=("01" "02" "03" "04")
# infiles
decade=("dec01" "dec02" "dec03" "dec04")
# full output has 14599 time steps.
# one member output has 1459 time steps.
# the times velow are for the first five ensemble members
#t1=(0 1460 2920 4380 5840)
#t2=(1458 2918 4378 5838 7298)
#yrs="_yr1-5"
#ensnum=("01" "02" "03" "04" "05")
# the times velow are for the second five ensemble members
#t1=(7300 8760 10220 11680 13140)
#t2=(8758 10218 11678 13138 14598)
#yrs="_yr6-10"
#ensnum=("06" "07" "08" "09" "10")

# use below to dramatically reduce file size by selecting the precip.
#ncks -v PRATEsfc /2005/dec01/autoregressive_predictions.nc -O autoregressive_predictions_2005_dec01_PRATEsfc.nc

# The 6 lines below extract the precipitation variable from the larger autoregressive_predictions file that is very large..
tcSeasons=("2005" "2013" "2024")
for i in ${tcSeasons[@]}; do 
  for j in ${decade[@]}; do
    echo 'do you need to grab only precip and rewrite the precip data to decades? '
#    ls -l ${origFiledir}'/'${i}/${j}/autoregressive_predictions.nc
#    ncks -v PRATEsfc ${origFiledir}'/'${i}/${j}/autoregressive_predictions.nc -O 'autoregressive_predictions_'${i}'_'${j}'_PRATEsfc.nc'
  done
done


# precip data is in autoregressive_predictions.nc file
#pfilein=${tcSeason}/${decade}'/autoregressive_predictions.nc'


#vtag="_PRATEsfc"
vtag="_TWP"
ftag="_b.nc" # normally this should be "_PRATEsfc.nc"

case "${tcSeason}" in
	"2005" | "2013")
          # use the timestamps below for 2005 and 2013
          echo "tcSeason is: "$tcSeason
          for blah in ${decnum[@]}; do
            ensnum="01"
            #ncks -d time,0,1458 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            #ncks -d time,0,1459 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,0,1459 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="02"
            #ncks -d time,1460,2918 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            #ncks -d time,1460,2919 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,1460,2919 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="03"
            #ncks -d time,2920,4378 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            #ncks -d time,2920,4379 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,2920,4379 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="04"
            #ncks -d time,4380,5838 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            #ncks -d time,4380,5839 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,4380,5839 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="05"
            #ncks -d time,5840,7298 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            #ncks -d time,5840,7299 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,5840,7299 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            #
            ensnum="06"
            #ncks -d time,7300,8759 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,7300,8759 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="07"
            #ncks -d time,8760,10219 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,8760,10219 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="08"
            #ncks -d time,10220,11679 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,10220,11679 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="09"
            #ncks -d time,11680,13139 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,11680,13139 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="10"
            #ncks -d time,13140,14599 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'${vtag}.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ##ncks -d time,13139,14598 'autoregressive_predictions_'${tcSeason}'_dec01${vtag}.nc' 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${ftag}
            ncks -d time,13139,14598 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
          done
	  ;;
	"2024")
          echo "tcSeason is: "$tcSeason
          # 2024 was a leap year and so should have 1464 6 hour chunks instead of 1460.  however, the output of ACE2 seems to have assumed that the output years 
          # are all the same length.  so it seems that 1464 6 hour chunks were written into the output arrays despite assuming that each year is 1460 chunks long.  
          # as a result, in the decade files, the last year does not appear to be complete, but rather 40 chunks too short.   this probably doesn't matter.  but it 
          # does influence which time stamps need to be used with ncks to get the individual years.  to have all the years the same length, we are dropping the 
          # last days (4 chunks), but that will mean that all of the timestamps after february 28th will be off by 1 day.  what a headache. 
          
          # the time stamps should be:  
          #a=np.array([0, 1464, 2928, 4392, 5856, 7320, 8784, 10248, 11712, 13176]) --> starting times
          #b=np.array([1459, 2923, 4387, 5851, 7315, 8779, 10243, 11707, 13171, 14635]) --> ending times
          
          # but, since the decadal output files only have 14600 6 hour chunks, the last starting and ending timestamps need to be: 
          #13131 and 14590
          # the above timestamps work, in that they produce an ensemble file with 1460 timesteps, but it is unsatisfying 
          # because the first many (40) timestamps are from the previous year, so all the dates are shifted by about 10 days.  
          
          # only use these numbers for 2024!!! or other leap years
          for blah in ${decnum[@]}; do
            ensnum="01"
            ncks -d time,0,1459 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="02"
            ncks -d time,1464,2923 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="03"
            ncks -d time,2928,4387 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="04"
            ncks -d time,4392,5851 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="05"
            ncks -d time,5856,7315 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            #
            ensnum="06"
            ncks -d time,7320,8779 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="07"
            ncks -d time,8784,10243 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="08"
            ncks -d time,10248,11707 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="09"
            ncks -d time,11712,13171 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
            ensnum="10"
            ncks -d time,13131,14590 'autoregressive_predictions_'${tcSeason}'_dec'${blah}${vtag}'.nc' -o 'autoregressive_predictions_'${tcSeason}'_dec'${blah}'_'${ensnum}${vtag}${ftag}
          done
	  ;;
	*)
	  echo "you haven't chosen an appropriate tcSeason you nimrod"
	  ;;
esac

# workflow: 

#  1.  data massaging 
# Precipitation
# 1 select precip variables from the full 'autoregressive_predictions.nc' files (seems like these are 10 year files)
# break each of these 10 year files into 1 year files so that we can composite the specific ensemble members.

# u-wind
# break each of the P-coord_ace2****yr1-5.n or *yr6-10.nc files into 1 year chuncks

# tc-count files
# compute the number of tcs per year, globally and basin-specific (which script does this?)
# break these values up into individual years (Mu-Ting had them all grouped together)

#  2.  run the RMM analysis for every ensemble member (120 of them)
#
# make a 3 panel plot showing TC counts as a function of MJO phase for each of 2005,2013, and 2024

#  3.  compute composites for each year of the difference between the top and bottom 5 or 10 ensemble members

cd ~/code/pythonCode/ACE2/

