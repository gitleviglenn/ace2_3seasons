#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ace2_climo_complot.py
#
# originally taken from ace2_mjo_complot.py
#
# this script creates several plots.   two plots show the TC count # as a function of MJO 
# phase with the first showing a plot for 5 select ensembles, and the second showing all
# 40 ensembles members from the particular year chosen.  
#
# then a series of three figures are creating showing the u850 and u200 zonal wind, and the
# precipitation, as a function of MJO phase (one map for each phase).  these panels plot 
# the mean fields from 5 ensemble members.  the variables plotted are: 
# comp_mn_u850, comp_mn_u200, and comp_mn_pr  
#
# ---- use ---
# source activate junky
# python ace2_complot.py   --> uses the default year, 2024
# to make plots for different years use: 
# python ace2_complot.py 2013
#
# levi silvers                                                 march 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# make some plots now
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
import sys
#sys.path.append('/barnes-engr-scratch1/c832572266/Function/')
sys.path.append('/home/C823281551/code/pythonCode/TC_genesis_ACE2_evaluation_public/function/')
from scipy import signal
#import KW_diagnostics as KW
import mjo_mean_state_diagnostics_uw as MJO
import os
import cartopy.util as cartopy_util
import cartopy.crs as ccrs
from datetime import datetime, timezone

yr_str    = '1'
#dirstr    = '/home/lsilvers/'
dirstr    = '/bell-scratch/C823281551/'
#dirstr2   = '/bell-scratch/C823281551/'
DIR       = dirstr + 'code/pythonCode/ACE2/'
file_dir  = DIR
file_dir2 = dirstr + 'data/ACE2/'

# Load basin info
basin_list    = list(['NI','NWPAC','NEPAC','NATL','SI','SPAC'])
basin_long_list = list(['North IO','North WestPac','North EastPac','North Atl','South IO','South Pac'])
basin_lon_min = np.array([45, 105, 180, 265, 35, 135])
basin_lon_max = np.array([105, 180, 265, 357.5, 135, 270])
latmax = 30 #25 is not used, use 30
basin_lat_min = np.array([0,    0,    0,  0,  -latmax, -latmax])
basin_lat_max = np.array([latmax,  latmax, latmax, latmax,    0, 0])
nbasin        = np.size(basin_list)

if len(sys.argv) > 1:
    yr2plot = sys.argv[1]
    print("scumstash says the year 2 plot is "+yr2plot+"...")
else: 
    yr2plot = '2024'
    print("scumstash says the year 2 plot is "+yr2plot+"...")

# /bell-scratch/C823281551/data/ACE2/MJO_8ph_composite_ACE2_2013_dec03_10_1yr.npz

# these are for the active years: 
if yr2plot == '2024':
    yr        = '2024'
    hinum = 9 # number of high end ensembles
    # 13, 0, 12, 34, 1
    #ensarr    = ['04', '01', '03', '05', '02']
    #decarr    = ['dec02', 'dec01', 'dec02', 'dec04', 'dec01']
    ensarr    = ['01',    '02',    '09',    '03',    '04',    '10',    '02',    '05',    '06']
    decarr    = ['dec01', 'dec01', 'dec01', 'dec02', 'dec02', 'dec03', 'dec04', 'dec04', 'dec04']
    # 0, 1, 8, 12, 13, 29, 31, 34, 35 --> additional ensembles (everything above 3rd quartile)
    # 1, 2, 9, 13, 14, 30, 32, 35, 36
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    hinum = 9 # number of high end ensembles
    # 8, 21, 17, 27, 28 
    #ensarr    = ['09', '02', '08', '08', '09']
    #decarr    = ['dec01', 'dec03', 'dec02', 'dec03', 'dec03']
    ensarr    = ['09'   , '01'   , '08'   , '01'   , '02'   , '08'   , '09'   , '04'   , '08']
    decarr    = ['dec01', 'dec02', 'dec02', 'dec03', 'dec03', 'dec03', 'dec03', 'dec04', 'dec04']
    # 8, 10, 17, 20, 21, 27, 28, 33, 37
    # 9, 11, 18, 21, 22, 28, 29, 34, 38
else:
    yr        = '2005'
    hinum = 7 # number of high end ensembles
    # 16, 1, 9, 2, 11
    #ensarr    = ['06', '01', '09', '02', '01']
    #decarr    = ['dec02', 'dec01', 'dec01', 'dec01', 'dec02']
    ensarr    = ['01'   , '02'   , '09'   , '01'   , '06'   , '05'   , '05']
    decarr    = ['dec01', 'dec01', 'dec01', 'dec02', 'dec02', 'dec03', 'dec04']
    # 0, 1, 8, 10, 15, 24, 34 --> additional ensembles (everything above the 3rd quartile)
    # 1, 2, 9, 11, 16, 25, 35

# these are for the inactive years: 

if yr2plot == '2024':
    yr        = '2024'
    lonum = 8 # number of low end ensembles
    # 33, 37, 5, 39, 7 --> shifted by +1 to match ensemble naming
    #ensarr_lo    = ['03', '07', '05', '09', '07']
    #decarr_lo    = ['dec04', 'dec04', 'dec01', 'dec04', 'dec01']
    ensarr_lo    = ['03',    '05',    '07',    '02',    '01',    '03',    '07',    '09']
    decarr_lo    = ['dec01', 'dec01', 'dec01', 'dec03', 'dec04', 'dec04', 'dec04', 'dec04']
    # 2, 4, 6, 21, 30, 32, 36, 38 --> additional ensembles (everything below 1st quartile)
    # 3, 4, 7, 22, 31, 33, 37, 39 --> shift by 1 to match the labelling of individual ensembles
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    lonum = 10 # number of low end ensembles
    # 20, 26, 32, 35, 15
    #ensarr_lo    = ['10', '06', '02', '05', '05']
    #decarr_lo    = ['dec02', 'dec03', 'dec04', 'dec04', 'dec02']
    ensarr_lo    = ['07'   , '05'   , '07'   , '10'   , '05'   , '06'   , '02'   , '03'   , '05'   , '10']
    decarr_lo    = ['dec01', 'dec02', 'dec02', 'dec02', 'dec03', 'dec03', 'dec04', 'dec04', 'dec04', 'dec04']
    # 6, 14, 16, 19, 24, 25, 31, 32, 34, 39
    # 7, 15, 17, 20, 25, 26, 32, 33, 35, 40 --> doubles the number of lower ensembles
else:
    yr        = '2005'
    lonum = 5 # number of low end ensembles
    # 23, 32, 20, 24, 40 
    ensarr_lo    = ['03',    '02',    '10',    '04',    '10']
    decarr_lo    = ['dec03', 'dec04', 'dec02', 'dec03', 'dec04']
    # 19, 22, 23, 31, 39
    # 20, 23, 24, 32, 40 --> same as bottom 5 members

#index = 8
#print('size and shape of u850_8ph are: ',np.size(u850_8ph),' and ',np.shape(u850_8ph))

#hinum = 9 # number of high end ensembles
#lonum = 8 # number of low end ensembles
hi_stars = np.zeros((hinum,8))
lo_stars = np.zeros((lonum,8))
all_stars = np.zeros((40,8))

# defines times at which the data is saved, for example, during the TC season (June 1st- Nov 30)
t1 = 604  # 604 corresponds roughly to June 1st
t2 = 1335 # 1335 corresponds roughly to November 30th.
tlength = t2-t1

nlat = 25
#nlat = 13

f1_var850  = np.zeros((hinum,tlength,nlat,144))
const_u850 = np.zeros((hinum,tlength,nlat,144))
const_u200 = np.zeros((hinum,tlength,nlat,144))
const_twp  = np.zeros((hinum,tlength,nlat,144))
const_vws  = np.zeros((hinum,tlength,nlat,144))

# for the low activity years:
const_u850_lo = np.zeros((lonum,tlength,nlat,144))
const_u200_lo = np.zeros((lonum,tlength,nlat,144))
const_twp_lo  = np.zeros((lonum,tlength,nlat,144))
const_vws_lo  = np.zeros((lonum,tlength,nlat,144))

#size and shape of u850_8ph are:  14976  and  (8, 13, 144)

# combine individual ensemble members into 1 array for processing. 
#########################################################################
# active years
for ind in range(0, hinum):
    ensnum  = ensarr[ind]
    dstr    = decarr[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    #file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
    file1   = 'int'+filstr+'u850_pm30.nc'
    file2   = 'int'+filstr+'u200_pm30.nc'
    file3   = 'int'+filstr+'TWP_b.nc'
    ds_f1   = xr.open_dataset(file_dir2+file1, decode_timedelta=True)
    ds_f2   = xr.open_dataset(file_dir2+file2, decode_timedelta=True)
    ds_f3   = xr.open_dataset(file_dir2+file3, decode_timedelta=True)
    temp1 = ds_f1['eastward_wind'] # temp1 is an xarray
    temp2 = ds_f2['eastward_wind'] # temp1 is an xarray
    temp3 = ds_f3['total_water_path'] # temp1 is an xarray
    #f1_var850[ind,:,:,:] = temp1[t1:t2,:,:]
    const_u850[ind,:,:,:] = temp1[t1:t2,:,:]
    const_u200[ind,:,:,:] = temp2[t1:t2,:,:]
    const_vws[ind,:,:,:]  = temp2[t1:t2,:,:] - temp1[t1:t2,:,:]
    const_twp[ind,:,:,:]  = temp3[0,t1:t2,:,:]
    print('file string',file1)

# inactive years
for ind in range(0, lonum):
    ensnum  = ensarr_lo[ind]
    dstr    = decarr_lo[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    file1   = 'int'+filstr+'u850_pm30.nc'
    file2   = 'int'+filstr+'u200_pm30.nc'
    file3   = 'int'+filstr+'TWP_b.nc'
    ds_f1   = xr.open_dataset(file_dir2+file1, decode_timedelta=True)
    ds_f2   = xr.open_dataset(file_dir2+file2, decode_timedelta=True)
    ds_f3   = xr.open_dataset(file_dir2+file3, decode_timedelta=True)
    temp1 = ds_f1['eastward_wind'] # temp1 is an xarray
    temp2 = ds_f2['eastward_wind'] # temp1 is an xarray
    temp3 = ds_f3['total_water_path'] # temp1 is an xarray
    print('temp1 shape',temp1)
    #f1_var850[ind,:,:,:] = temp1[t1:t2,:,:]
    const_u850_lo[ind,:,:,:] = temp1[t1:t2,:,:]
    const_u200_lo[ind,:,:,:] = temp2[t1:t2,:,:]
    const_vws_lo[ind,:,:,:]  = temp2[t1:t2,:,:] - temp1[t1:t2,:,:]
    const_twp_lo[ind,:,:,:]  = temp3[0,t1:t2,:,:]
    print('file string',file1)
#########################################################################

# These are individual files, mostly for testing purposes...
filenc   = file_dir2+'int'+filstr+'u200_pm30.nc'
file2nc  = file_dir2+'int'+filstr+'u850_pm30.nc'
file3nc  = file_dir2+'autoregressive_predictions'+filstr+'PRATEsfc_b.nc'
file4nc  = file_dir2+'int'+filstr+'TWP_b.nc'
ds       = xr.open_dataset(filenc, decode_timedelta=True)
ds2      = xr.open_dataset(file2nc, decode_timedelta=True)
ds3      = xr.open_dataset(file3nc, decode_timedelta=True)
ds4      = xr.open_dataset(file4nc, decode_timedelta=True)
lat      = ds['lat']
lon      = ds['lon']
var200   = ds['eastward_wind']
var850   = ds2['eastward_wind']
varTWPa  = ds4['total_water_path']
varpr    = ds3['PRATEsfc']
lat3     = ds3['lat']
lon3     = ds3['lon']
lat4     = ds4['lat']
lon4     = ds4['lon']
temptime = ds['time']
#time     = temptime[0:endtime]
vname = list(['varpr','var850','var200'])

#vrpr = varpr[1,:,:,:]
#varTWP = varTWPa[1,:,:,:]

# average over time
v200_mn  = np.mean(var200,axis=0)
v850_mn  = np.mean(var850,axis=0)
vTWP_mn  = np.mean(varTWPa,axis=1)
varpr_mn = np.mean(varpr,axis=1)

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('files are: ',filenc)
print('files are: ',file2nc)
print('files are: ',file3nc)
print('files are: ',file4nc)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('file string for Fig1 is: ',filstr)
print('size and shape of var200 are: ',np.size(var200),' and ',np.shape(var200))
print('size and shape of mn var200 are: ',np.size(v200_mn),' and ',np.shape(v200_mn))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('size and shape of var850 are: ',np.size(var850),' and ',np.shape(var850))
print('size and shape of mn var850 are: ',np.size(v850_mn),' and ',np.shape(v850_mn))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
#print('size and shape of vTWP are: ',np.size(varTWP),' and ',np.shape(varTWP))
print('size and shape of mn vTWP are: ',np.size(vTWP_mn),' and ',np.shape(vTWP_mn))
print('size adn shape of lon4 are: ',np.size(lon4),' and ',np.shape(lon4))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('size and shape of precip are: ',np.size(varpr),' and ',np.shape(varpr))
print('size and shape of mn precip are: ',np.size(varpr_mn),' and ',np.shape(varpr_mn))
print('size adn shape of lon3 are: ',np.size(lon3),' and ',np.shape(lon3))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')


print('size of const_u200 is: ',np.shape(const_u850))
comp_ensmn_u850 = np.mean(const_u850,axis=0) # average over the ensemble members
comp_mn_u850 = np.mean(comp_ensmn_u850,axis=0) # average over the ensemble members

comp_ensmn_u200 = np.mean(const_u200,axis=0) # average over the ensemble members
comp_mn_u200 = np.mean(comp_ensmn_u200,axis=0) # average over the ensemble members

comp_ensmn_vws  = np.mean(const_vws,axis=0) # average over the ensemble members
comp_mn_vws  = np.mean(comp_ensmn_vws,axis=0) # average over the ensemble members

comp_ensmn_twp  = np.mean(const_twp,axis=0) # average over the ensemble members
comp_mn_twp  = np.mean(comp_ensmn_twp,axis=0) # average over the ensemble members

print('size of comp_mn_u200 is: ',np.shape(comp_mn_u850))
#
comp_ensmn_lo_u850 = np.mean(const_u850_lo,axis=0) # average over the ensemble members
comp_mn_lo_u850 = np.mean(comp_ensmn_lo_u850,axis=0) # average over the ensemble members

comp_ensmn_lo_u200 = np.mean(const_u200_lo,axis=0) # average over the ensemble members
comp_mn_lo_u200 = np.mean(comp_ensmn_lo_u200,axis=0) # average over the ensemble members

comp_ensmn_lo_vws  = np.mean(const_vws_lo,axis=0) # average over the ensemble members
comp_mn_lo_vws  = np.mean(comp_ensmn_lo_vws,axis=0) # average over the ensemble members

comp_ensmn_lo_twp  = np.mean(const_twp_lo,axis=0) # average over the ensemble members
comp_mn_lo_twp  = np.mean(comp_ensmn_lo_twp,axis=0) # average over the ensemble members

# compute the difference between hi and lo ensemble members

comp_diff_u850 = comp_mn_u850 - comp_mn_lo_u850
comp_diff_u200 = comp_mn_u200 - comp_mn_lo_u200
comp_diff_vws  = comp_mn_vws - comp_mn_lo_vws
comp_diff_twp  = comp_mn_twp - comp_mn_lo_twp

for ind in range(0, lonum):
    ensnum  = ensarr_lo[ind]
    dstr    = decarr_lo[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
    fa      = np.load(file_dir2+file)
    TC_fa   = fa['TC_genesis_MJO_phase_basin']
    lo_stars[ind,:] = TC_fa[:,3]
    print(fa.files)
    print('file string',filstr)
    print('index is',ensarr_lo[ind])

mn_lo_stars = np.mean(lo_stars,axis=0) # compute the mean value along each MJO phase
mn_lo_stars

# go big or go home 
# print out the filstr for all 40 ensembles, as a check. 
totind=0
ensarr    = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
decarr    = ['dec01', 'dec02', 'dec03', 'dec04']
for ind in range(0, 10):
    ensnum  = ensarr[ind]
    for ind2 in range(0, 4):
        dstr    = decarr[ind2]
        filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
        file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
        fa      = np.load(file_dir2+file)
        TC_fa   = fa['TC_genesis_MJO_phase_basin']
        all_stars[totind,:] = TC_fa[:,3]
        #print(fa.files)
        print('file string',filstr)
        #print('ense index is',ensarr[ind])
        #print('dec index is',decarr[ind2])
        totind = totind + 1

mn_all_stars = np.mean(all_stars,axis=0) # compute the mean value along each MJO phase
mn_all_stars

##############################
# looks like we don't need the meshgrid variables???
lon_tmp = lon
lat_tmp = lat
[xx, yy] = np.meshgrid(lon_tmp, lat_tmp)

lon3_tmp = lon3
lat3_tmp = lat3
[xx3, yy3] = np.meshgrid(lon3_tmp, lat3_tmp)

lon4_tmp = lon4
lat4_tmp = lat4
[xx4, yy4] = np.meshgrid(lon4_tmp, lat4_tmp)

#cbar = "RdBu"
##        cbar = "RdBu_r"
#        scalef = 86400.
scalef = 1.
##
##model_name = 'ERA5'
##cmap_list = list(['RdBu','RdBu_r','RdBu_r'])
cmap_list = 'RdBu_r'
cmap_2    = 'BrBG'
cmap_bl   = 'Blues'
##
### Set Contour Level
clev3 = np.arange(-2,2.5,0.25) # pr
cticks3 = np.arange(-2,2.75,1)
#clev3 = np.arange(-3,3.5,0.5) # pr
#cticks3 = np.arange(-3,4,1)
clev2 = np.arange(-20,21,2) # u850
cticks2 = np.arange(-20,21,2)
clev1 = np.arange(-10, 11, 1) # u200
cticks1 = np.arange(-10, 12, 2)
clev4 = np.arange(0,61,2) # u850
cticks4 = np.arange(0,61,4)

##############################
# below is code for figures based on multiple ensemble members
fig_name  = 'Fig_wind_water_Comp_Hi_'+yr+'_4pan_pm30.png'
fig, axes = plt.subplots(4,1,figsize=(6.5, 7),dpi=600, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.9, wspace=0.1)
plt.rcParams.update({'font.size': 7})

plt.subplot(4,1,1)
ax = plt.gca()
ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 mn (ACE2)', y=0.96)
#
print('size of comp_mn_u200 is: ',np.shape(comp_mn_u200))
contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_u200, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

##########
plt.subplot(4,1,2)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
#ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
#ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['20S','10S', '0', '10N', '20N', '30N'], fontsize=6)
#ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u850 mn (ACE2)', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_u850, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

plt.suptitle('mean of active ensemble members', y=0.96)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

##########
plt.subplot(4,1,3)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
#ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
#ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['20S','10S', '0', '10N', '20N', '30N'], fontsize=6)
#ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 - u850', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_vws, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev2, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
#cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks2)

##########
plt.subplot(4,1,4)
ax = plt.gca()

ax.coastlines(color='grey', linewidth=0.75)
#ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['20S','10S', '0', '10N', '20N', '30N'], fontsize=6)
plt.title('TWP', y=0.96)

contour = plt.contourf(
    lon4_tmp, lat4_tmp, scalef*comp_mn_twp, cmap=cmap_bl,
    transform=ccrs.PlateCarree(), levels= clev4, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks4)

plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
###

##################
# below is code for figures based on multiple ensemble members
fig_name  = 'Fig_wind_water_Comp_Lo_'+yr+'_4pan_pm30.png'
fig, axes = plt.subplots(4,1,figsize=(6.5, 7),dpi=600, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.9, wspace=0.1)
plt.rcParams.update({'font.size': 7})

plt.subplot(4,1,1)
ax = plt.gca()
ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 mn (ACE2)', y=0.96)
#
contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_lo_u200, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

##########
plt.subplot(4,1,2)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
#ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u850 mn (ACE2)', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_lo_u850, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

plt.suptitle('mean of quiet ensemble members', y=0.96)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

##########
plt.subplot(4,1,3)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_yticks(np.arange(-30,40,10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 - u850', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_mn_lo_vws, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev2, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
#cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks2)

##########
plt.subplot(4,1,4)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
#ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20,30,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['20S','10S', '0', '10N', '20N'], fontsize=6)
plt.title('TWP', y=0.96)

contour = plt.contourf(
    lon4_tmp, lat4_tmp, scalef*comp_mn_lo_twp, cmap=cmap_bl,
    transform=ccrs.PlateCarree(), levels= clev4, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks4)

plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
###

##################################

print('lon_tmp and lat_tmp are: ',lon_tmp[:])
print('lat_tmp is:',lat_tmp[:])
ln1 = 105
ln2 = 143
lt1 = 12
lt2 = 24
lon_tmp2 = lon_tmp[ln1:ln2]
lat_tmp2 = lat_tmp[lt1:lt2]
##################################
# below is code for figures based on the difference of  multiple ensemble members
fig_name  = 'Fig_wind_water_Comp_diff_'+yr+'_4pan_window.png'
fig, axes = plt.subplots(4,1,figsize=(7.5, 10.0),dpi=900, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
#plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.6, wspace=0.1)
plt.rcParams.update({'font.size': 7})

fsize=8
plt.subplot(4,1,1)
ax = plt.gca()
ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(180,360,30), crs=ccrs.PlateCarree())
#ax.set_yticks(np.arange(0,30,10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['180', '150W', '120W', '90W', '60W', '30W'], fontsize=fsize)
#ax.set_yticklabels(['0', '10N', '20N'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N', '20N', '30N'], fontsize=fsize)
plt.title('u200 mn (ACE2)', y=0.96)
#
contour = plt.contourf(
        lon_tmp, lat_tmp, scalef*comp_diff_u200, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev3, extend='both'
)
ax.set_extent([60, 180, 0, 30], crs=ccrs.PlateCarree(central_longitude=180))

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=8)
cb.set_ticks(cticks3)

##########
plt.subplot(4,1,2)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(180,360,30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['180', '150W', '120W', '90W', '60W', '30W'], fontsize=fsize)
#ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N', '20N', '30N'], fontsize=fsize)
plt.title('u850 mn (ACE2)', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_diff_u850, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev3, extend='both'
)
ax.set_extent([60, 180, 0, 30], crs=ccrs.PlateCarree(central_longitude=180))

plt.suptitle('mean of quiet ensemble members', y=0.96)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
#cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks3)

##########
plt.subplot(4,1,3)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(180,360,30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['180', '150W', '120W', '90W', '60W', '30W'], fontsize=fsize)
#ax.set_yticklabels(['0', '10N', '20N'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N', '20N', '30N'], fontsize=fsize)
plt.title('u200 - u850', y=0.96)

contour = plt.contourf(
    lon_tmp, lat_tmp, scalef*comp_diff_vws, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev3, extend='both'
)
ax.set_extent([60, 180, 0, 30], crs=ccrs.PlateCarree(central_longitude=180))

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
#cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
#cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks3)

##########
plt.subplot(4,1,4)
ax = plt.gca()

ax.set_aspect('2.0')
ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(180,360,30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,40,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['180', '150W', '120W', '90W', '60W', '30W'], fontsize=fsize)
ax.set_yticklabels(['10S', '0', '10N', '20N', '30N'], fontsize=fsize)
plt.title('TWP', y=0.96)

contour = plt.contourf(
    lon4_tmp, lat4_tmp, scalef*comp_diff_twp, cmap=cmap_2,
    transform=ccrs.PlateCarree(), levels= clev3, extend='both'
)
ax.set_extent([60, 180, 0, 30], crs=ccrs.PlateCarree(central_longitude=180))

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
#cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks3)

plt.savefig(fig_name,format='png', dpi=900) # Change this to be fig_dir_ace2 if using ace data
###
#
##############################
##############################

V1 = v200_mn[:,:]
V2 = v850_mn[:,:]
VWS = V1[:,:] - V2[:,:]
V3 = varpr_mn[0,:,:]
V4 = vTWP_mn[0,:,:]

# below is code for figures based on 1 ensemble member
fig_name  = 'Fig_wind_water_1yr'+filstr+'4pan_pm30.png'
fig, axes = plt.subplots(4,1,figsize=(6.5, 7),dpi=600, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.9, wspace=0.1)
plt.rcParams.update({'font.size': 7})

plt.subplot(4,1,1)
ax = plt.gca()

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('size and shape of V2 are: ',np.size(V2),' and ',np.shape(V2))
print('size and shape of V3 are: ',np.size(V3),' and ',np.shape(V3))
print('size and shape of V4 are: ',np.size(V4),' and ',np.shape(V4))
print('size and shape of VWS are: ',np.size(VWS),' and ',np.shape(VWS))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')

# Handle the data to prevent white line
[V_tmp1_cyclic, lon_cyclic] = cartopy_util.add_cyclic_point(
      V1.T,
      coord=lon_tmp,
      axis=0
)

[V_tmp2_cyclic, lon_cyclic] = cartopy_util.add_cyclic_point(
      V2.T,
      coord=lon_tmp,
      axis=0
)

# VWS 
[V_tmp3_cyclic, lon_cyclic] = cartopy_util.add_cyclic_point(
      VWS.T,
      coord=lon_tmp,
      axis=0
)

# TWP
[V_tmp4_cyclic, lon4_cyclic] = cartopy_util.add_cyclic_point(
      V4.T,
      coord=lon4_tmp,
      axis=0
)

# precipitation
[V_tmp5_cyclic, lon3_cyclic] = cartopy_util.add_cyclic_point(
      V3.T,
      coord=lon3_tmp,
      axis=0
)

ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 mn (ACE2)', y=0.96)
#
# Plot the data
contour = plt.contourf(
    lon_cyclic, lat_tmp, scalef*V_tmp1_cyclic.T, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

#plt.suptitle('Fig1 MJO composite test (ACE2)', y=0.96)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

#########
plt.subplot(4,1,2)
ax = plt.gca()

ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('v850 mn (ACE2)', y=0.96)

contour = plt.contourf(
    lon_cyclic, lat_tmp, scalef*V_tmp2_cyclic.T, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev1, extend='both'
)

plt.suptitle('Fig1 1 year', y=0.96)

#cb = fig.colorbar(contour, ax=axes[:], orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.05, aspect=40)
#cb.ax.tick_params(labelsize=6)
#cb.set_ticks(cticks3)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks1)

##########
plt.subplot(4,1,3)
ax = plt.gca()

ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)
plt.title('u200 - v850', y=0.96)

contour = plt.contourf(
    lon_cyclic, lat_tmp, scalef*V_tmp3_cyclic.T, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev2, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks2)

##########
plt.subplot(4,1,4)
ax = plt.gca()

ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20,30,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['20S','10S', '0', '10N', '20N'], fontsize=6)
plt.title('TWP', y=0.96)

contour = plt.contourf(
    lon4_cyclic, lat4_tmp, scalef*V_tmp4_cyclic.T, cmap=cmap_bl,
    transform=ccrs.PlateCarree(), levels= clev4, extend='both'
)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.15, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks4)

##
plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data


##### new figure
fig_name  = 'Fig_precip_Comp'+filstr+'1pan_pm30.png'
fig, axes = plt.subplots(1,1,figsize=(6.5, 7),dpi=600, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.9, wspace=0.1)
plt.rcParams.update({'font.size': 7})

plt.subplot(1,1,1)
ax = plt.gca()

ax.coastlines(color='grey', linewidth=0.75)
ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)

scalep = 86400.
contour = plt.contourf(
    lon3_cyclic, lat3_tmp, scalep*V_tmp5_cyclic.T, cmap=cmap_list,
    transform=ccrs.PlateCarree(), levels= clev3, extend='both'
)
plt.title('precip (ACE2, 1yr)', y=0.96)
plt.suptitle('Precipitation (ACE2, 1yr)', y=0.96)

cb = fig.colorbar(contour, ax=ax, orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.2, aspect=40)
cb.ax.tick_params(labelsize=6)
cb.set_ticks(cticks3)
plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data


plt.close()

