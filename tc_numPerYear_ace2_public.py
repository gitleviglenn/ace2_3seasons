#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# tc_numPerYear_ace2_lgs.py
#
# goal: count the number of TCs per year, then pick out the top years and the bottom years
#       based on the tc count.  preparation to make composite plots
#
# as written originally, computes the number of TCs globally 
# for all of the ensemble members of a given year.   thus for the year 2013, the 
# number of TC 'snapshots' will be the total number, over the whole globe, summed over
# all 40 ensemble members.   so that final ntc number should be divided by 40 and that 
# will give the global number of TCs, which for 2013 is on the order of: 70 storms
#
# to do:  print out numbers for individual basins, then strip down this script so that
#         it will work for one ensemble member at a time.   
#
# levi silvers                                            dec 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.util as cartopy_util
import cartopy.crs as ccrs
from netCDF4 import Dataset
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#yr_str    = '1'
dirstr    = '/home/'
dirstr1   = '.'
dirstr2   = '.'
DIR       = dirstr + 'code/'
#
file_dir  = dirstr2 + 'data/ACE2/'
file_dir2 = dirstr2 + 'ACE2/testout/'
file_dir3 = dirstr + 'data/ACE2/'
#
fig_dir_ace2 = dirstr2 + 'figure/ace2_fig/'
file_dir_era5_eof = dirstr2 + 'data/ACE2/'
file_dir_out = file_dir_era5_eof
year = '2013'

#/bell-scratch/C837469599/
dirTC = 'ACE2_share/Tracked_TC/StichNodes/'

dir_in  = dirstr1 + dirTC  


print('path: ',dir_in)
#print('filename is: ',filename)
print('stupid is as stupid does ')
print('no Diggity')

expname_list = list(['ace2'])

#---------------------------------------------------------------------------------------
def print_npz_contents(filename):
    try:
        # Use a 'with' statement to ensure the file is closed automatically
        with np.load(filename, allow_pickle=True) as data:
            print(f"Contents of '{filename}':")
            print("-" * 30)

            # Check the names of the arrays stored in the file
            array_names = data.files
            print(f"Array names (keys): {array_names}\n")

            if not array_names:
                print("The .npz file contains no arrays.")
                return

            # Iterate through each array and print its content
            for name in array_names:
                print(f"--- Array '{name}' ---")
                array_data = data[name]
                print(f"Shape: {array_data.shape}")
                print(f"Dtype: {array_data.dtype}")
                print("Data:")
                # Printing large arrays might be verbose; adjust print options if needed
                print(array_data)
                print("\n")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

## Replace 'your_file.npz' with the path to your actual file
#if __name__ == "__main__":
#    print_npz_contents('your_file.npz')

#---------------------------------------------------------------------------------------
tcSeasonyr = ['2005', '2013', '2024']
tcDecade   = ['dec01', 'dec02', 'dec03', 'dec04']
tcTmpYr    = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
    

def is_header(line):
    return line.strip().startswith("start")

#for first_time_execution in range(1,-1,-1):
#    print('first_time_execution',first_time_execution)
#    for icase in range(0,1):
#        expname = expname_list[icase]
#        fig_dir = DIR + 'figure/ace2_fig/TC/'
#        os.makedirs(fig_dir, exist_ok=True)
#
#        # Name of the sub directory for the data named "filename"
#        # dir_sub_list = list(['yr1','yr2-5','yr6-10'])
#        dir_sub_list = list(['dec01','dec02','dec03','dec04'])
#
#        nsub = np.size(dir_sub_list)
#        print('nsub is: ',nsub)
#        for imem in range(0, 1):#nmem):
#            mem_str = f"{imem+1:02d}"
#            for isub in range(0, nsub):
#                decname = dir_sub_list[isub]
#
#                #filename = 'tracks.ACE2.TC.'+mem_str+'.'+yrname+'.txt'
#                filename = 'tracks.ACE2.TC.10yr.'+year+'.'+decname+'.txt'
#                print('isub is: ',isub)
#                print('filename is: ',filename)

# Load basin info
basin_list    = list(['NI','NWPAC','NEPAC','NATL','SI','SPAC'])
basin_long_list = list(['North IO','North WestPac','North EastPac','North Atl','South IO','South Pac'])
basin_lon_min = np.array([45, 105, 180, 265, 35, 135])
basin_lon_max = np.array([105, 180, 265, 357.5, 135, 270])
latmax = 30 #25 is not used, use 30
basin_lat_min = np.array([0,    0,    0,  0,  -latmax, -latmax])
basin_lat_max = np.array([latmax,  latmax, latmax, latmax,    0, 0])
nbasin        = np.size(basin_list)
 
numTCensemble         = np.empty([40]) 
numTCensembleBasin    = np.empty([40]) 
num1         = np.empty([3,40]) 
num2         = np.empty([3,40]) 
numTCensemble[:]      = np.nan
numTCensembleBasin[:] = np.nan

# we also need to break up the incoming wind and precip data into 1 year chunks....
#iens = 0
for iyr in range(0,3):
    iens = 0
    iy = tcSeasonyr[iyr]
    #print('****************************')
    #print('Simulation Year, iyr is: ',iy)
    #print('****************************')
    for idc in range(0,4):
        idec = tcDecade[idc]
        print('tc decade is: ',idec)
        for ityr in range(0,10):
            ity = tcTmpYr[ityr]
            filename = file_dir2+'TC_genesis_1yr_'+iy+'_'+idec+'_'+ity+'.0_ace2.npz'
            #print('tmp year is: ',ity)
            #print('tc gen incoming f is: '+file_dir2+'TC_genesis_1yr_'+iy+'_'+idec+'_'+ity+'.0_ace2.npz')

            # Define expected number of columns in your data rows
            expected_columns = 11  # Adjust this based on your actual data

            # Define a list to hold valid data rows
            data_rows = []

            # Read file line by line
            #print('dir plus filen',dir_in+decname+'/'+filename)
            #with open(dir_in+decname+'/'+filename, "r") as file:
            #with open(filename, "r") as file:
            with np.load(filename) as file:
                #print(f"Contents of '{filename}':")
                #print_npz_contents(filename)
                data_mslp = file["mslp"]
                lon_TC  = file["lon_TC"]
                lat_TC  = file["lat_TC"]
                #print(f"Shape: {data_mslp.shape}")
                bo = np.shape(data_mslp)
                boo = bo[0]
                #print('boo is: ',boo)
                #print("-" * 30)
                #ibasin = basin_list[3]
                ibasin = 3
                counter = 0
                for i in range(0, np.size(lon_TC)):
                    #counter = 0
                    #for ibasin in range(0, nbasin):
                    dlonmin = lon_TC[i]-basin_lon_min[ibasin]
                    dlonmax = lon_TC[i]-basin_lon_max[ibasin]
                    dlatmin = lat_TC[i]-basin_lat_min[ibasin]
                    dlatmax = lat_TC[i]-basin_lat_max[ibasin]
                    #print(dlonmin, dlonmax, dlatmin, dlatmax)
                    if dlonmin*dlonmax < 0 and dlatmin*dlatmax <0:
                        counter = counter + 1
                        #TC_genesis_MJO_phase_basin[iph, ibasin] = TC_genesis_MJO_phase_basin[iph, ibasin] + 1
                #print('counter is: ',counter)
                numTCensembleBasin[iens] = counter
                numTCensemble[iens] = boo 
                iens = iens + 1
                #print(ibasin)
    num1[iyr,:] = numTCensembleBasin[:]
    print('numTCensembleBasin is: ',numTCensembleBasin)
    print('****************************')
    print('Simulation year is: ',iy)
    print('****************************')
    print('numTCensemble is: ',np.sort(numTCensemble))
    print('sorted numTCensembleBasin is: ',np.sort(numTCensembleBasin))
    print('unsorted numTCensembleBasin is: ',numTCensembleBasin)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('size of numTCensembleBasin is: ',np.shape(numTCensembleBasin))
    print('numTCensembleBasin is: ',numTCensembleBasin[0:5])
    print('numTCensembleBasin is: ',numTCensembleBasin[5:10])
    print('numTCensembleBasin is: ',numTCensembleBasin[10:15])
    print('numTCensembleBasin is: ',numTCensembleBasin[15:20])
    print('numTCensembleBasin is: ',numTCensembleBasin[20:25])
    print('numTCensembleBasin is: ',numTCensembleBasin[25:30])
    print('numTCensembleBasin is: ',numTCensembleBasin[30:35])
    print('numTCensembleBasin is: ',numTCensembleBasin[35:41])
    #print('what is it? ',numTCensembleBasin)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    quartiles = np.quantile(numTCensembleBasin, [0.25, 0.5, 0.75])
    std_test  = np.std(numTCensembleBasin)
    print(f"Q1, Median, Q3: {quartiles}")
    print(f"std is: {std_test}")
    print(f"first element of quartiles is: ",quartiles[0])
    print(f"second element of quartiles is: ",quartiles[1])
    print(f"third element of quartiles is: ",quartiles[2])
    print('---------------------------------------------')
    print(f"1.5 std - mean is: ",quartiles[2] - 1.5*std_test)
    print(f"1.5 std + mean is: ",1.5*std_test + quartiles[2])
    print('---------------------------------------------')
    print(f"std - mean is: ",quartiles[2] - std_test)
    print(f"std + mean is: ",std_test + quartiles[2])
    print('---------------------------------------------')

    indAAA = np.where(numTCensembleBasin > quartiles[2])
    indBBB = np.where(numTCensembleBasin < quartiles[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Simulation year is: ',iy)
    print('indices where num of TC genesis is greater than the third quartile are: ',indAAA)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('indices where num of TC genesis is less than the third quartile are: ',indBBB)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    #indices = [i for i, n in enumerate(numTCensembleBasin) if n >=4]
    tcmin = np.min(numTCensembleBasin)
    tcmax = np.max(numTCensembleBasin)
    print(iy, 'max index is: ',np.max(numTCensembleBasin))
    indices = [i for i, n in enumerate(numTCensembleBasin) if n >= tcmax - np.rint(std_test)]
    print(iy,': indices of ensemble members with TC count above 4 are: ',indices)
    indices = [i for i, n in enumerate(numTCensembleBasin) if n <= tcmin + np.rint(std_test)]
    print(iy,': indices of ensemble members with TC count below -1 std are: ',indices)

