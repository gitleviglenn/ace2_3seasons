# this script opens a txt file that contains data from 10 ensembles of a given year
# and breaks the data up into 10 individual npz files that each contain data from 
# one ensemble member.   this script needs to be run for each 10 ensemble file for
# each of the 3 years that that were simulated for the Silvers et al ACE2 3 seasons
# paper.
#
# levi silvers

import numpy as np
import xarray as xr
import pandas as pd

dirstr1   = '.'
dirTC = 'ACE2_share/Tracked_TC/StichNodes/'
dir_in  = dirstr1 + dirTC  
dir_out = '.'

# example file in: 
#filein = 'dec01/tracks.ACE2.TC.10yr.2005.dec01.txt'

tcseason = '2005' # '2013', '2024'
decade   = '03' # '01', '02', '04'
DIR = dir_in + 'dec'+decade+'/'
filename = 'tracks.ACE2.TC.10yr.'+tcseason+'.dec'+decade+'.txt' 

print('dir_in:',dir_in)

fig_dir_ace2 = dir_out

expected_columns = 11
data_rows  = []

def is_header(line):
    return line.strip().startswith("start")
#

with open(DIR+filename, "r") as file: 
    lines = file.readlines() # creates a list of strings, with each element being one line from 'file'
    for i, line in enumerate(lines):
        if is_header(line):
            #print('is_header! and length of lines is: ',len(lines))
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                columns = next_line.split()

                data_rows.append(columns)
                #print('index is: ',i)

data = pd.DataFrame(data_rows, dtype=float)
print('first 6 rows of data: ',data.head(6))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# list the years desired: 
listyr = [2001.0, 2002.0, 2003.0, 2004.0, 2005.0, 2006.0, 2007.0, 2008.0, 2009.0, 2010.0]

#data2 = data[(data[7] == 2005.0)]
for iyr in range(0,10):
    print('iyr is: ',iyr,' and listyr is: ',listyr[iyr])
    stryr = str(listyr[iyr])
    data2 = data[(data[7] == listyr[iyr])]
    print('first 3 rows of data2: ',data2.head(3))
    mslp1, yr1 = data2[4], data2[7]
    lon_TC_a, lat_TC_a, mslp_a, vmax_a, hsfc_a = data2[2], data2[3], data2[4], data2[5], data2[6]
    yr_a, mon_a, day_a, hr_a                   = data2[7],data2[8], data2[9], data2[10]
    np.savez(fig_dir_ace2+'TC_genesis_1yr_'+tcseason+'_dec'+decade+'_'+stryr+'_ace2.npz', lon_TC = lon_TC_a, lat_TC=lat_TC_a, \
             mslp=mslp_a, vmax=vmax_a, hsfc=hsfc_a, yr=yr_a, mon=mon_a, day=day_a, hr=hr_a)


print('anxiety saved here: ',fig_dir_ace2)






