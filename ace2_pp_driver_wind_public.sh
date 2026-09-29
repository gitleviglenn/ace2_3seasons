#!/usr/bin/env bash

# this script separates files with 5 ensembles into files with 1 ensemble.  
# this script operates on 1 year at a time, set by the tcSeason variable.

# what a disgraceful mess this is.     levi silvers

# input:  ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 
# output: 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}

wkdir='/data/ACE2'
cd $wkdir

echo 'working directory is: '
echo $wkdir

tcSeason="2013"
#decnum="01"
decnum=("04" "02" "03" "01")
# infiles
#decade=("dec01" "dec02" "dec03" "dec04")
# full output has 14599 time steps.
# one member output has 1459 time steps.
# the times velow are for the first five ensemble members
#t1=(0 1460 2920 4380 5840)
#t2=(1458 2918 4378 5838 7298)
#yrs="_yr1-5"
#ensnum=("01" "02" "03" "04" "05")
# the times velow are for the second five ensemble members, only needed for the precipitation
# files which have 10 instead of 5 members
# t1=(7300 8760 10220 11680 13140)
# t2=(8758 10218 11678 13138 14598)
yrs="_yr6-10"
#yrs="_yr1-5"
#ftag="_b.nc" # usually this will be just ".nc"
ftag="_pm30.nc" # usually this will be just ".nc"
#
#ensnum=("06" "07" "08" "09" "10")

#
#filein=${tcSeason}/${decade}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc'
# precip data is in autoregressive_predictions.nc file
#pfilein=${tcSeason}/${decade}'/autoregressive_predictions.nc'
#
#

case "${tcSeason}" in
	"2005" | "2013")
          # use the timestamps below for 2005 and 2013
          echo "tcSeason is: "$tcSeason
          ## for years 1-5: 
          vars=("u850" "u200")
	  case "${yrs}" in 
		  "_yr1-5")
	            echo "years being used are: ${yrs}"
                    for toast in ${vars[@]}; do
                        for blah in ${decnum[@]}; do
                          #ensnum="01"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,0,1458 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,0,1459 ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="02"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,1460,2918 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,1460,2919 ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,1460,2919 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="03"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,2920,4378 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,2920,4379 ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,2920,4379 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="04"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,4380,5838 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,4380,5839 ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,4380,5839 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="05"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5840,7299 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5840,7298 'int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5839,7298 ${origFiledir}${tcSeason}'/dec'${blah}'/pressure_coordinate/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,5839,7298 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5840,7299 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                        done
                    done
		    ;;
		  "_yr6-10")
	            echo "years being used are: ${yrs}"
                    for toast in ${vars[@]}; do
                        for blah in ${decnum[@]}; do
                          #ensnum="06"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                    #     # ncks -d time,0,1459 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="07"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                    #     # ncks -d time,1460,2919 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,1460,2919 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="08"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                    #     # ncks -d time,2920,4379 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,2920,4379 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,2920,4379 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ensnum="09"
                          #echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                    #     # ncks -d time,4380,5839 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ##ncks -d time,4380,5839 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,4380,5839 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="10"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                    #      ncks -d time,5839,7298 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5839,7298 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,5839,7298 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                        done
                    done
		    ;;
		  *)
	            echo "years being used are probably garbage" 
		    ;;
          esac
	  ;;
	"2024")
	  echo "tcSeason is: "${tcSeason}
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
          echo "tcSeason is: "$tcSeason
          ## for years 1-5: 
          vars=("u850" "u200")
	  case "${yrs}" in 
		  "_yr1-5")
	            echo "years being used are: ${yrs}"
                    for toast in ${vars[@]}; do
                        for blah in ${decnum[@]}; do
                          ensnum="01"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="02"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,1464,2923 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="03"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,2928,4387 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="04"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,4392,5851 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="05"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,5840,7299 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
	                done
                    done
		    ;;
		  "_yr6-10")
	            echo "years being used are: ${yrs}"
                    for toast in ${vars[@]}; do
                        for blah in ${decnum[@]}; do
                          ensnum="06"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="07"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,1464,2923 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="08"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,2928,4387 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="09"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,4392,5851 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ensnum="10"
                          echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          #ncks -d time,5840,7299 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
                          ncks -d time,5839,7298 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}${ftag} 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
	                done
                    done
		    ;;
		  *)
	            echo "years being used are probably garbage" 
		    ;;
          esac
	  ;;
	*)
	  echo "you haven't chosen an appropriate tcSeason you nimrod"
	  ;;
esac

### for years 6-10: 
### decade 4 has a slightly different path (one directory up)
#vars=("u850" "u200")
#for toast in ${vars[@]}; do
#    for blah in ${decnum[@]}; do
#      ensnum="06"
#      echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
##      ncks -d time,0,1459 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ncks -d time,0,1459 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ensnum="07"
#      echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
##      ncks -d time,1460,2919 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ncks -d time,1460,2919 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ensnum="08"
#      echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
##      ncks -d time,2920,4379 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ncks -d time,2920,4379 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ensnum="09"
#      echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
##      ncks -d time,4380,5839 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ncks -d time,4380,5839 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ensnum="10"
#      echo 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
##      ncks -d time,5839,7298 ${origFiledir}${tcSeason}'/dec'${blah}'/P-coord_ace2_u_'${tcSeason}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#      ncks -d time,5839,7298 ${wkdir}'/int_'${toast}'_'${tcSeason}'dec'${blah}${yrs}'.nc' 'int_'${tcSeason}'_dec'${blah}'_'${ensnum}'_'${toast}${ftag}
#    done
#done

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

