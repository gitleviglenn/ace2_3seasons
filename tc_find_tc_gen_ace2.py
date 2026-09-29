#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# makes mulitple plots with strange names.   one of which is a violin plot for ace2.
#
# all of the figures display distributions of the ace2 ensembles that have been run 
# for 2005, 2013, or 2024.
#
# howl2.png: a 3 panel plot showing the TC# generated in each of the 40 ensembles
# for each of the three seasons, in the Atlantic basin.  
#
# wildeyes.png: a 1 panel plot that plots the data in howl2.png on one plot with 
# each season a different color.
#
# arghblah.png: a 1 panel plot that plots the TC geneis numbers for all 120 ensemble 
# members with each season indicated by a different color. 
#
# mfmlfy.png: a 1 panel violin plot showing the distribution of TC# across the 40
# ensemble members for each season, and for all seasons together. 
#
# levi silvers                                                                 april 2026
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
dirstr    = '/home/lsilvers/'
dirstr1   = '/bell-scratch/C837469599/'
dirstr2   = '/bell-scratch/C823281551/'
DIR       = dirstr + 'code/pythonCode/ACE2/'
expname_list = list(['ace2'])
#
file_dir  = dirstr2 + 'data/ACE2/'
#
file_dir3 = dirstr + 'data/ACE2/'
fig_dir   = dirstr2 + 'figure/ace2_fig/'
file_dir_era5_eof = dirstr2 + 'data/ACE2/'
file_dir_out = file_dir_era5_eof

#year = '2013'

#/bell-scratch/C837469599/
dirTC = 'ACE2_share/Tracked_TC/StichNodes/'

dir_in  = dirstr1 + dirTC  

file_dir_out_mem01 = file_dir_out  
sub_dir_list = list(['2005','2013','2024'])

os.makedirs(file_dir_out, exist_ok=True)
os.makedirs(fig_dir, exist_ok=True)

imin = 0
nsub = np.size(sub_dir_list)
imem = 0

latmax                 = 30

# Define a function to detect headers (customize this logic for your case)
def is_header(line):
    # Example: Headers start with "start"
    return line.strip().startswith("start")

for first_time_execution in range(1,0,-1):#-1,-1):
    print(first_time_execution)
    for icase in range(0,1):
        expname = expname_list[icase]

        for isub in range(0,3):#imin, 2):#nsub):#nsub):
            sub_dir = sub_dir_list[isub]


            for idec in range(0, 4):#4):
                dec_str = f"{idec+1:02d}"
                dir_in_sub = dir_in + 'dec' + dec_str + '/'

                filename = 'tracks.ACE2.TC.10yr.'+sub_dir+'.dec'+dec_str+'.txt'

                # Define expected number of columns in your data rows
                expected_columns = 11  # Adjust this based on your actual data

                # Define a list to hold valid data rows
                data_rows = []

                print(dir_in+filename)

                # Read file line by line
                with open(dir_in_sub+filename, "r") as file:

                    lines = file.readlines()
                    #print(lines)
                    for i, line in enumerate(lines):
                        if is_header(line):  # Detect a header
                            #print('is_header!')
                            if i + 1 < len(lines):  # Ensure the next line exists
                                next_line = lines[i + 1].strip()
                                # Split the next line into columns
                                columns = next_line.split()  # Customize split logic if needed
                                #print('columns:',columns)

                                data_rows.append(columns)  # Only append if it's the next line of header

                # Convert the filtered rows to a DataFrame
                data = pd.DataFrame(data_rows, dtype=float)


                # If you want to assign each column to a separate variable
                lon_TC, lat_TC, mslp, vmax_10m, hsfc = data[2], data[3], data[4], data[5], data[6],  # Adjust depending on the number of columns
                yr, mon, day, hr           = data[7], data[8], data[9], data[10]

                if isub == 0:
                    ist = 0
                    if first_time_execution == 1:
                        TC_genesis = np.empty(nsub, dtype=int)
                TC_genesis[isub] = np.size(lon_TC)


                ist = ist + TC_genesis[isub]
                # Save data
                np.savez(file_dir_out+'TC_genesis_'+sub_dir+'_dec'+dec_str+'.npz', lon_TC = lon_TC, lat_TC=lat_TC, mslp=mslp,\
                        vmax_10m=vmax_10m, hsfc=hsfc, yr=yr, mon=mon, day=day, hr=hr)

            ntc = np.sum(TC_genesis)


for isub in range(0, 3):
    sub_dir = sub_dir_list[isub]
    for idec in range(0, 4):
        dec_str = f"{idec+1:02d}"
        
        data = np.load(file_dir_out+'TC_genesis_'+sub_dir+'_dec'+dec_str+'.npz')
        yr = data['yr']
        mon = data['mon']
        lon_TC = data['lon_TC']
        lat_TC = data['lat_TC']

        for iyr in range(0, 10):
            if iyr == 0 and idec==0 and isub==0:
                TC_num = np.empty([40, 3])
            TC_num[iyr+idec*10, isub] = np.sum(yr==iyr+2001) #+yr_begin)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIGURE

plt.plot(TC_num[:,0], 'bo')
plt.xlabel('Ensemble member')
plt.ylabel('Number of TC genesis per year')
plt.plot(TC_num[:,1], 'ro')
plt.plot(TC_num[:,2], 'ko')
plt.xticks(np.arange(0,45,5))
plt.title('Global TC genesis count')
plt.savefig('arghblah.png', dpi=300)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Separate TC number for each basin
# Define basin
basin_list    = list(['NI','NWPAC','NEPAC','NATL','SI','SPAC'])
basin_long_list = list(['North IO','North WestPac','North EastPac','North Atl','South IO','South Pac'])
basin_lon_min = np.array([45, 105, 180, 265, 35, 135])
basin_lon_max = np.array([105, 180, 265, 357.5, 135, 270])
latmax = 30 #25 is not used, use 30
basin_lat_min = np.array([0,    0,    0,  0,  -latmax, -latmax])
basin_lat_max = np.array([latmax,  latmax, latmax, latmax,    0, 0])
nbasin        = np.size(basin_list)

for isub in range(0, 3):
    sub_dir = sub_dir_list[isub]

    for idec in range(0, 4):

        if idec == 0:
            TC_genesis_yr_basin_ace2 = np.zeros([40, nbasin])
        dec_str = f"{idec+1:02d}"

        # Load TC genesis data from each year
        data = np.load(file_dir_out+'TC_genesis_'+sub_dir+'_dec'+dec_str+'.npz')
        #data = np.load(file_dir_out+'TC_genesis_'+str(yr_begin)+'_'+str(yr_last)+'.npz')

        # Assign basin index
        lon_TC   = data['lon_TC']
        lat_TC   = data['lat_TC']
        yr_TC = data['yr']
        #if iexp == 0:
        basin_id_ace2 = np.zeros([np.size(lon_TC)])
        basin_id_ace2[:] = np.nan
        #else:
        #    basin_id_era5 = np.zeros([np.size(lon_TC)])
        #    basin_id_era5[:] = np.nan

        for i in range(0, np.size(lon_TC)):
            for ibasin in range(0, nbasin):
                #print(i, ibasin)
                if ( (lon_TC[i]-basin_lon_min[ibasin])*(basin_lon_max[ibasin]-lon_TC[i]) >= 0 ) and \
                    ( (lat_TC[i]-basin_lat_min[ibasin])*(basin_lat_max[ibasin]-lat_TC[i]) >= 0 ):
                    #if iexp == 0:
                    basin_id_ace2[i] = ibasin
                    #elif iexp == 1:
                    #    basin_id_era5[i] = ibasin
                    #print(ibasin)
                    break
        
        for i in range(0, np.size(yr_TC)):
            if np.isnan(basin_id_ace2[i]) != 1:

                imem = int(yr_TC[i]-2001)+idec*10

                ibasin  = int(basin_id_ace2[i])

                TC_genesis_yr_basin_ace2[ imem, ibasin] = TC_genesis_yr_basin_ace2[ imem, ibasin] + 1

    # Save data
    mem = np.arange(0, 40)
    np.savez(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir+'.npz', 
            TC_genesis_yr_basin_ace2 = TC_genesis_yr_basin_ace2,\
            basin_list = basin_list, basin_long_list=basin_long_list,\
            basin_lon_min = basin_lon_min, basin_lon_max = basin_lon_max, \
            basin_lat_min = basin_lat_min, basin_lat_max = basin_lat_max,\
            mem = mem) # (mem, basin)
else:
    data = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir+'.npz')
    TC_genesis_yr_basin_ace2 = data['TC_genesis_yr_basin_ace2']
    mem = data['mem']
    basin_list = data['basin_list']
    basin_long_list = data['basin_long_list']
    nbasin = np.size(basin_list)


# plot TC genesis number for Atlantic 

expname = list(['2005','2013','2024'])
iplt_atl = 3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIGURE

# the figure below, howl2.png generates a 3 panel plot showing the TC# generated in each of the 40 ensembles
# for each of the three seasons, in the Atlantic basin.  

fig, ax = plt.subplots(1,3,figsize=(6.5, 4),dpi=600)
#plt.subplots_adjust(left=0.14, right=0.98,top=0.90,bottom=0.05,hspace=0.3, wspace=0.2)
plt.subplots_adjust(left=0.14, right=0.98,top=0.50,bottom=0.05,hspace=0.3, wspace=0.2)
plt.rcParams.update({'font.size': 7})
#ax[0].set_aspect('2.0')
#ax[1].set_aspect('2.0')
#ax[2].set_aspect('2.0')

xindex=np.arange(0,40,1) # use if switching axes is desired
for isub in range(0, 3):
    sub_dir = sub_dir_list[isub]
    data = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir+'.npz')
    TC_genesis_yr_basin_ace2 = data['TC_genesis_yr_basin_ace2']

    plt.subplot(1, 3, isub+1)
    #ax[isub].set_aspect('equal') # i am struggling to get this to work..
    plt.plot(TC_genesis_yr_basin_ace2[:,iplt_atl], 'bo', markersize=2)
    #plt.plot(TC_genesis_yr_basin_ace2[:,iplt_atl],xindex, 'bo', markersize=2)
    plt.xlabel('Ensemble member')
    if isub == 0:
        plt.ylabel('Number of TC genesis per year')
    plt.xticks(np.arange(0,45,5))
    #plt.xticks(np.arange(3,20,1))
    plt.title(expname[isub])
    plt.ylim([4, 20])
    #plt.ylim([0, 40])

fig.suptitle('Atlantic annual TC number')
fig.savefig('howl2.png', dpi=300)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#------------------------------------
# work on plotting all three years on same plots, as 'violin' plots
data1 = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir_list[0]+'.npz')
TC_genesis_yr1_basin_ace2 = data1['TC_genesis_yr_basin_ace2']
data2 = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir_list[1]+'.npz')
TC_genesis_yr2_basin_ace2 = data2['TC_genesis_yr_basin_ace2']
data3 = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir_list[2]+'.npz')
TC_genesis_yr3_basin_ace2 = data3['TC_genesis_yr_basin_ace2']

# concatinate all ensemble members into one dataset
master_TC = np.concatenate((TC_genesis_yr1_basin_ace2[:,iplt_atl],TC_genesis_yr2_basin_ace2[:,iplt_atl],TC_genesis_yr3_basin_ace2[:,iplt_atl]), axis=None)

master_data = [TC_genesis_yr1_basin_ace2[:,iplt_atl],TC_genesis_yr2_basin_ace2[:,iplt_atl],TC_genesis_yr3_basin_ace2[:,iplt_atl],master_TC]
positions = [1,3,5,7]

# compute percentiles
tmp = [np.percentile(data,[25,50,75]) for data in master_data]

def get_whisker(tmp,master_data):
    whisker = []
    for quantile,data in zip(tmp,master_data):
        data = np.array(data)
        q1 = quantile[0]
        median = quantile[1]
        q3 = quantile[2]
        iqr = q3 - q1
        upper = q3 + 1.5 * iqr
        upper = np.clip(upper,q3,data.max())
        lower = q1 - 1.5 * iqr
        lower = np.clip(lower,data.min(),q1)
        whisker.append((upper,lower))
    return whisker

whisker = get_whisker(tmp,master_data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIGURE

# this figure is a 1 panel violin plot
fig,ax = plt.subplots()
#colors = ['gold','skyblue','lightcoral','grey']
#colors = ['#ffab0f','#75bbfd','#f6688e','#ada587']
colors = ['#ffab0f','#82cafc','#ff796c','#ada587']
#colors = ['#fec615','#95d0fc','#fe7b7c','#d8dcd6']
#vp = ax.violinplot(dataset=master_data,positions=[1,3,5,7], bw_method=0.25, facecolor=['gold','skyblue','lightcoral','grey'])
vp = ax.violinplot(dataset=master_data,positions=[1,3,5,7], bw_method=0.25)
for i, body in enumerate(vp['bodies']):
#for body in vp['bodies']:
    #body.set_facecolor(['gold','skyblue','lightcoral','grey'])
    #body.set_facecolor('grey')
    body.set_facecolor(colors[i])
vp['cmaxes'].set_color('black')
vp['cmins'].set_color('black')
vp['cbars'].set_color('black')
plt.ylabel('# of TCs per year', fontsize=14)
plt.xlabel('year', fontsize=14)
ax.scatter(positions,
        [quantile[1] for quantile in tmp],
        marker='D',color='black',s=45,zorder=3)
ax.vlines(positions,
        [quantile[0] for quantile in tmp],
        [quantile[2] for quantile in tmp],
        color='black',linestyle='-',lw=5)
plt.xticks(positions, ['2005','2013','2024','total'], fontsize=14)
plt.yticks(fontsize=14)
fig.savefig('mfmlfy.png', dpi=300)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#----------------------------------

coldots = ['bo', 'ro', 'ko']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIGURE

# this figure make a 1 panel plot showing the Atlantic basin TC
# genesis numbers for all 120 ensemble members, with each season
# indicated by a different color. 

fig = plt.figure(figsize=(16, 14))
for isub in range(0, 3):
    sub_dir = sub_dir_list[isub]
    data = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir+'.npz')
    TC_genesis_yr_basin_ace2 = data['TC_genesis_yr_basin_ace2']

    #fig = plt.figure(figsize=(12, 12))
    plt.plot(TC_genesis_yr_basin_ace2[:,3], coldots[isub])
    plt.xlabel('Ensemble member')
    plt.ylabel('Number of TC genesis per year')
    plt.xticks(np.arange(0,45,5))
    plt.title('stop')
    plt.savefig('wildeyes.png', dpi=300)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TC_genesis_all3 = np.zeros([120, nbasin])
#fig = plt.figure(figsize=(16, 14))
#print('TC_genesis_all3 shape: ',np.shape(TC_genesis_all3))
#i1=0
#i2=39
#for isub in range(0, 3):
#    print('i1 is: ',i1,' and i2 is: ',i2)
#    sub_dir = sub_dir_list[isub]
#    data = np.load(file_dir_out + 'TC_genesis_number_yr_basin_ace2_'+sub_dir+'.npz')
#    TC_genesis_temp = data['TC_genesis_yr_basin_ace2']
#    print('temp shape is: ',np.shape(TC_genesis_temp))
#    TC_genesis_all3[i1:i2+1,:] = data['TC_genesis_yr_basin_ace2']
#    i1 = i2+1
#    i2 = i2+40 
#    plt.hist( TC_genesis_all3[:,3], bins = np.arange(0,20,0.5))
#    plt.savefig('saveface.png', dpi=300)
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#print('TC_genesis is: ',TC_genesis_all3[:,3])
print('hey scumstash, figs should be here: ',os.getcwd())

