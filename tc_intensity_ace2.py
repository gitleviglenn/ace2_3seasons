#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# tc_intensity_ace2.py
#
# goal: plot 2 measures (vmax and mslp) of the intensity of TCs
#
# separate out results according to the different basins.  use code from 
# C2.1_TC_genesis_seasonal_interannual_2001_2010 as an initial guide.
#
# this is a pretty crapy script because i am still learning python, numpy and pandas
#
# produces a 2 panel figure with histograms of vmax and mslp for a 
# particular year. 
#
# levi silvers                                      dec 2025
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
yr_str    = '1'
dirstr    = '/home/lsilvers/'
dirstr1   = '/bell-scratch/C837469599/'
dirstr2   = '/bell-scratch/C823281551/'
DIR       = dirstr + 'code/pythonCode/ACE2/'
#
file_dir  = dirstr2 + 'data/ACE2/'
#
file_dir3 = dirstr + 'data/ACE2/'
fig_dir_ace2 = dirstr2 + 'figure/ace2_fig/'
file_dir_era5_eof = dirstr2 + 'data/ACE2/'
file_dir_out = file_dir_era5_eof
dstr  = 'dec01'
dstr2 = 'dec02'
dstr3 = 'dec03'
dstr4 = 'dec04'
year = '2005'
mem_str = year

#/bell-scratch/C837469599/
dirTC = 'ACE2_share/Tracked_TC/StichNodes/'


dir_in  = dirstr1 + dirTC  

#filename  =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr+'.txt'
#filename2 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr2+'.txt'
#filename3 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr3+'.txt'
#filename4 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr4+'.txt'

fig_name = 'Fig_TC_intensity_histogram_'+mem_str+'_4decs_50bns.png' #'_'+yrname+'.png'

print('path: ',dir_in)
#print('filename is: ',filename)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define basin
basin_list    = list(['NI','NWPAC','NEPAC','NATL','SI','SPAC'])
basin_long_list = list(['North IO','North WestPac','North EastPac','North Atl','South IO','South Pac'])
basin_lon_min = np.array([45, 105, 180, 265, 35, 135])
basin_lon_max = np.array([105, 180, 265, 357.5, 135, 270])
latmax = 30 #25 is not used, use 30
basin_lat_min = np.array([0,    0,    0,  0,  -latmax, -latmax])
basin_lat_max = np.array([latmax,  latmax, latmax, latmax,    0, 0])
nbasin        = np.size(basin_list)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print('NATL: ',basin_list[3])
print('NATL lon min/max: ',basin_lon_min[3],' ',basin_lon_max[3])
print('NATL lat min/max: ',basin_lat_min[3],' ',basin_lat_max[3])
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# open each of the above files, read data row by row and save in a 
# DataFrame
# 
# after all files (probably 4) are read into DataFrames concatinate 
# them all into a single DataFrame for analysis.

expected_columns = 11
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
year = '2005'
mem_str = year

filename  =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr+'.txt'
filename2 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr2+'.txt'
filename3 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr3+'.txt'
filename4 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr4+'.txt'

print('filename is: ',filename)

dir_str_list = list([dstr,dstr2,dstr3,dstr4])
file_str_list = list([filename,filename2,filename3,filename4])
data  = pd.DataFrame()
data2 = pd.DataFrame()
data3 = pd.DataFrame()
data4 = pd.DataFrame()
datarows_list = list([data, data2, data3, data4])

# Read file line by line
for i in range(0,4):
    data_rows = []
    with open(dir_in+dir_str_list[i]+'/'+file_str_list[i], "r") as file:
        for line in file:
            # Split the line by whitespace
            columns = line.strip().split()
            # Check if the line matches the expected column count
            if len(columns) == expected_columns:
                try:
                    # Attempt to convert the first value to a float (filter out header rows)
                    float(columns[0])
                    data_rows.append(columns)  # Only append if it's not a header
                    #print('size of data_rows is: ',np.shape(data_rows))
                except ValueError:
                    print('what?????')
                    # Skip the line if the first item is not numeric (header row)
                    continue
    ## Convert the filtered rows to a DataFrame for each of the four decades
    datarows_list[i] = pd.DataFrame(data_rows, dtype=float)

#datarows_list[i] = pd.DataFrame(data_rows, dtype=float)
dataConc = pd.concat([datarows_list[0], datarows_list[1], datarows_list[2], datarows_list[3]])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
year = '2013'
mem_str = year

filename  =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr+'.txt'
filename2 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr2+'.txt'
filename3 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr3+'.txt'
filename4 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr4+'.txt'

print('filename is: ',filename)

dir_str_list = list([dstr,dstr2,dstr3,dstr4])
file_str_list = list([filename,filename2,filename3,filename4])
data  = pd.DataFrame()
data2 = pd.DataFrame()
data3 = pd.DataFrame()
data4 = pd.DataFrame()
datarows_list = list([data, data2, data3, data4])

# Read file line by line
for i in range(0,4):
    data_rows = []
    with open(dir_in+dir_str_list[i]+'/'+file_str_list[i], "r") as file:
        for line in file:
            # Split the line by whitespace
            columns = line.strip().split()
            # Check if the line matches the expected column count
            if len(columns) == expected_columns:
                try:
                    # Attempt to convert the first value to a float (filter out header rows)
                    float(columns[0])
                    data_rows.append(columns)  # Only append if it's not a header
                    #print('size of data_rows is: ',np.shape(data_rows))
                except ValueError:
                    print('what?????')
                    # Skip the line if the first item is not numeric (header row)
                    continue
    ## Convert the filtered rows to a DataFrame for each of the four decades
    datarows_list[i] = pd.DataFrame(data_rows, dtype=float)

#datarows_list[i] = pd.DataFrame(data_rows, dtype=float)
dataConc2013 = pd.concat([datarows_list[0], datarows_list[1], datarows_list[2], datarows_list[3]])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
year = '2024'
mem_str = year

filename  =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr+'.txt'
filename2 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr2+'.txt'
filename3 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr3+'.txt'
filename4 =  'tracks.ACE2.TC.10yr.'+year+'.'+dstr4+'.txt'

print('filename is: ',filename)

dir_str_list = list([dstr,dstr2,dstr3,dstr4])
file_str_list = list([filename,filename2,filename3,filename4])
data  = pd.DataFrame()
data2 = pd.DataFrame()
data3 = pd.DataFrame()
data4 = pd.DataFrame()
datarows_list = list([data, data2, data3, data4])

# Read file line by line
for i in range(0,4):
    data_rows = []
    with open(dir_in+dir_str_list[i]+'/'+file_str_list[i], "r") as file:
        for line in file:
            # Split the line by whitespace
            columns = line.strip().split()
            # Check if the line matches the expected column count
            if len(columns) == expected_columns:
                try:
                    # Attempt to convert the first value to a float (filter out header rows)
                    float(columns[0])
                    data_rows.append(columns)  # Only append if it's not a header
                    #print('size of data_rows is: ',np.shape(data_rows))
                except ValueError:
                    print('what?????')
                    # Skip the line if the first item is not numeric (header row)
                    continue
    ## Convert the filtered rows to a DataFrame for each of the four decades
    datarows_list[i] = pd.DataFrame(data_rows, dtype=float)

#datarows_list[i] = pd.DataFrame(data_rows, dtype=float)
dataConc2024 = pd.concat([datarows_list[0], datarows_list[1], datarows_list[2], datarows_list[3]])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


print('shape1: ',datarows_list[1].shape,' 2:',datarows_list[0].shape,' Conc:',dataConc.shape)
print('type of data: ',type(data))
print('first 5 rows of data: ',datarows_list[1].head())
print('last 10 rows of data: ',data.tail(10))
print('info of data: ',data.info())

# interesting possibility for pandas stats: 
# data['column name'].quantile([0.25, 0.75])
# data[[list of column names by string]].agg(['mean','min','max'])
# also see here: https://www.youtube.com/watch?v=DkjCaAMBGWM
# data[[list of column names by string]].agg(
#{'column name': ['mean','min','max'],
# 'column2 name': ['mean'],
# 'column3 name': ['min','max']
# }
#)

 
# If you want to assign each column to a separate variable
#lon_TC, lat_TC, mslp, vmax, hsfc  = data[2], data[3], data[4], data[5], data[6]  
                #yr, mon, day, hr       = data[8], data[9], data[10], data[11]

mslp_Conc, vmax_Conc = dataConc[4], dataConc[5]

print('====================================')
print(dataConc)
#dataConc['dataConc'].agg(['mean','min','max'])
#print(dataConc['1'].mean())
dataConc.columns = ['lon1','lat1','lon2','lat2','mnpress','Vmax','seven','eight','nine','ten','hour']
dataConc2013.columns = ['lon1','lat1','lon2','lat2','mnpress','Vmax','seven','eight','nine','ten','hour']
dataConc2024.columns = ['lon1','lat1','lon2','lat2','mnpress','Vmax','seven','eight','nine','ten','hour']
print('====================================')
column_names = dataConc.columns
print('column names are: ',column_names)
print('====================================')
print('stats of Vmax: ',dataConc['Vmax'].agg(['mean','min','max']))
print('stats of mslp: ',dataConc['mnpress'].agg(['mean','min','max']))
print('====================================')
print('====================================')
print('nope: ',dataConc.query('(Vmax > 25.)'))
print('====================================')
print('====================================')
print('nope: ',dataConc.query('(mnpress < 95000.)'))
print('====================================')
print('====================================')
basin_lat_mn = 0
basin_lat_mx = 30
basin_lon_mn = 265
basin_lon_mx = 357.5
print('max/min lat2:',dataConc['lat2'].agg(['mean','min','max']))
print('max/min lon2:',dataConc['lon2'].agg(['mean','min','max']))
#print('query Basin: ',dataConc.query('(lat2 > @basin_lat_mn) and (lat2 < @basin_lat_mx) and (lon2 > @basin_lon_mn) and (lon2 < @basin_lon_mx)'))
print('====================================')
#print(dataConc[''].mean())

data_atl = dataConc.query('(lat2 > @basin_lat_mn) and (lat2 < @basin_lat_mx) and (lon2 > @basin_lon_mn) and (lon2 < @basin_lon_mx)')
data_atl_2013 = dataConc2013.query('(lat2 > @basin_lat_mn) and (lat2 < @basin_lat_mx) and (lon2 > @basin_lon_mn) and (lon2 < @basin_lon_mx)')
data_atl_2024 = dataConc2024.query('(lat2 > @basin_lat_mn) and (lat2 < @basin_lat_mx) and (lon2 > @basin_lon_mn) and (lon2 < @basin_lon_mx)')
print('====================================')
print('2005 stats of Vmax in the atlantic: ',data_atl['Vmax'].agg(['mean','min','max']))
print('2005 stats of mslp in the atlantic: ',data_atl['mnpress'].agg(['mean','min','max']))
print('====================================')
print('2013 stats of Vmax in the atlantic: ',data_atl_2013['Vmax'].agg(['mean','min','max']))
print('2013 stats of mslp in the atlantic: ',data_atl_2013['mnpress'].agg(['mean','min','max']))
print('====================================')
print('2024 stats of Vmax in the atlantic: ',data_atl_2024['Vmax'].agg(['mean','min','max']))
print('2024 stats of mslp in the atlantic: ',data_atl_2024['mnpress'].agg(['mean','min','max']))
print('====================================')
vmaxThrs = 25.
pminThrs = 96000.
data_atl_int1 = dataConc.query('(Vmax > @vmaxThrs)')
data_atl_thsh_2013 = data_atl_2013.query('(Vmax > @vmaxThrs)')
data_atl_thsh_2024 = data_atl_2024.query('(Vmax > @vmaxThrs)')
data_atl_int2 = dataConc.query('(mnpress < @pminThrs)')
data_atl_int2_2013 = data_atl_2013.query('(mnpress < @pminThrs)')
data_atl_int2_2024 = data_atl_2024.query('(mnpress < @pminThrs)')
print('====================================')
print('query vmaxThrs in 2005: ',data_atl_int1.query('(Vmax > @vmaxThrs)'))
print('***********************====================================')
print('query vmaxThrs in 2013: ',data_atl_2013.query('(Vmax > @vmaxThrs)'))
print('***********************====================================')
print('query vmaxThrs in 2024: ',data_atl_2024.query('(Vmax > @vmaxThrs)'))
print('***********************====================================')
print('stats of Vmax above @vmaxThrs in the atlantic: ',data_atl_int1['Vmax'].agg(['mean','min','max']))
print('====================================')
print('query pminThrs in 2005: ',data_atl_int1.query('(mnpress < @pminThrs)'))
print('***********************====================================')
print('query pminThrs in 2013: ',data_atl_2013.query('(mnpress < @pminThrs)'))
print('***********************====================================')
print('query pminThrs in 2024: ',data_atl_2024.query('(mnpress < @pminThrs)'))
print('***********************====================================')
print('====================================')
print('query pminThrs: ',dataConc.query('(mnpress < @pminThrs)'))
print('stats of mean central pressure below ',pminThrs,' in the atlantic: ',data_atl_int2['mnpress'].agg(['mean','min','max']))
print('====================================')



print('save output figure to: /bell-scratch/C823281551/data/ACE2/')
print('or maybe here: ',fig_dir_ace2)

fig, ax = plt.subplots(1,2,figsize=(5.5, 3.5),dpi=600)
plt.subplots_adjust(left=0.1, right=0.98,top=0.8,bottom=0.15,hspace=0.3, wspace=0.24)
plt.rcParams.update({'font.size': 7})
plt.suptitle('TC intensity: , '+mem_str, y=1.002, fontsize=11 )
#
plt.subplot(1,2,1)
plt.title('Maximum windspeed at 10m')
#plt.hist(vmax, bins = np.arange(0,50,2))
plt.hist(vmax_Conc, bins = np.arange(0,50,1))
plt.xlabel('vmax (m/s)')
plt.ylabel('# of TC snapshots')
#
plt.subplot(1,2,2)
plt.title('Minimum sea level pressure')
#plt.hist(mslp/100, bins = np.arange(890,1014,2))
plt.hist(mslp_Conc/100, bins = np.arange(890,1014,2))
plt.xlabel('mslp (hPa)')
plt.ylabel('# of TC snapshots')
plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600)
#plt.show()

# histograms for the Atlantic basin
fig_name = 'Fig_TC_intensity_histogram_Atlantic_'+mem_str+'_4decs_50bns.png' #'_'+yrname+'.png'
fig, ax = plt.subplots(1,2,figsize=(5.5, 3.5),dpi=600)
plt.subplots_adjust(left=0.1, right=0.98,top=0.8,bottom=0.15,hspace=0.3, wspace=0.24)
plt.rcParams.update({'font.size': 7})
plt.suptitle('TC intensity: , '+mem_str, y=1.002, fontsize=11 )
#
plt.subplot(1,2,1)
plt.title('Atlantic Maximum windspeed at 10m')
#plt.hist(vmax, bins = np.arange(0,50,2))
plt.hist( data_atl['Vmax'], bins = np.arange(0,50,1))
plt.xlabel('vmax (m/s)')
plt.ylabel('# of TC snapshots')
#
plt.subplot(1,2,2)
plt.title('Atlantic Minimum sea level pressure')
#plt.hist(mslp/100, bins = np.arange(890,1014,2))
plt.hist(data_atl['mnpress']/100, bins = np.arange(890,1014,2))
plt.xlabel('mslp (hPa)')
plt.ylabel('# of TC snapshots')
plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600)
#plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

# histograms for the Atlantic basin
fig_name = 'Fig_TC_intensity_AtlanticB_'+mem_str+'_4decs.png' #'_'+yrname+'.png'
#
figB, ax = plt.subplots(figsize = (6,4))
ax.set_xlim(0, 40)
#ax.set_aspect('equal')
ax.set_xlabel("Vmax (m/s)")
#ax.set_xlabel("Tangential Wind (m/s)", fontsize=14)
data_atl['Vmax'].plot(kind = "kde", label="2005")
data_atl_2013['Vmax'].plot(kind = "kde", label="2013")
data_atl_2024['Vmax'].plot(kind = "kde", label="2024")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600)

# histograms for the Atlantic basin
fig_name = 'Fig_TC_vmax_hist_Atlantic_4decs.png' #'_'+yrname+'.png'

binnum = 30 # was 30
order = [0, 2, 1]
#figB, ax = plt.subplots(figsize = (6,4))
figB, ax = plt.subplots()
#ax.set_aspect('0.1')
ax.set_aspect(0.04)
#data_atl_2024['Vmax'].plot(kind = "hist", bins = binnum, color="lightcoral", label="2024") # ind 0
#data_atl_2024['Vmax'].plot(kind = "hist", bins = binnum, color="xkcd:#ff796c", label="2024") # ind 0
data_atl_2024['Vmax'].plot(kind = "hist", bins = binnum, color="xkcd:salmon", label="2024") # ind 0
ax.set_xlim(0, 40)
#ax.set_xlabel("Vmax (m/s)")
ax.set_xlabel("Tangential Wind (m/s)", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)
data_atl['Vmax'].plot(kind = "hist", bins = binnum, color="gold", label="2005") # ind 1
#data_atl['Vmax'].plot(kind = "hist", bins = binnum, color="#ffab0f", label="2005") # ind 1
#data_atl_2013['Vmax'].plot(kind = "hist", bins = binnum, color="skyblue", label="2013") # ind 2
data_atl_2013['Vmax'].plot(kind = "hist", bins = binnum, color="#82cafc", label="2013") # ind 2
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
handles, labels = ax.get_legend_handles_labels()
plt.legend([handles[i] for i in order], [labels[i] for i in order],fontsize=12)
plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600)

# histograms for the Atlantic basin
fig_name = 'Fig_TC_intensity_PDF_Atlantic_mnpress_4decs.png' #'_'+yrname+'.png'
#
figB, ax = plt.subplots(figsize = (6,4))
ax.set_xlim(94000, 103000)
ax.set_xlabel("min pressure (hPa)")
data_atl['mnpress'].plot(kind = "kde", label="2005")
data_atl_2013['mnpress'].plot(kind = "kde", label="2013")
data_atl_2024['mnpress'].plot(kind = "kde", label="2024")
plt.legend()
plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600)





