####################################################################################################
# find_rmm_1yr.py
#
# data from ACE2 has been restructured to have individual files for each ensemble member (1 yr).
# the wind and precipitation data files are here: 
#    /bell-scratch/C823281551/data/ACE2/
#        autoregressive_predictions_2024_dec02_09_PRATEsfc.nc --> 1 ensemble member each file
#        int_u850_2013dec01_yr6-10.nc --> 5 ensemble members each
#
# the TC number data files are here: 
#    /bell-scratch/C823281551/ACE2/testout/
#
# output data files(e.g. filename.npz) from this script appear to be going here: 
#    /bell-scratch/C823281551/data/ACE2/
#
# loosely following E1.1_Find_rmm_ace2_2001_2010.ipynb
# originally written by Mu-Ting Chien
#
# to run this script, the 'junky' environment needs to be activated with 
# $ source activate junky
#
# then run something like this, choosing the desired year and decade tag.
#
# syntax: 
# python find_rmm_1yr.py loki 2005 dec01 01
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Scripts needed for data prep before running this file: 
#    tc_numPerYear_ace2.py  --> computes the TC genesis data and stores it in an npz file
#    interp_ace2_maui.py    --> interpolates the incoming wind and precip data
#
# E1.1_Find_rmm_ace2_2001_2010.ipynb is really just the last part of the analysis and doesn't reveal 
# much about the data preparation.  there is some data prep, in the removal of the 120 running mean
# but not much else.  
# Much of the data prep seems to have been done in the notebooks: 
#    C4.2_Calc_TCGI_anomaly.py
#    D1.2_Tropical_wave_ace2.py
#
#    The TC genesis data is computed with this script: tc_numPerYear_ace2.py 
#    Output from tc_numPerYear_ace2.py is stored in this file: 
#    tc_genesis_file='/bell-scratch/C823281551/data/ACE2/TC_genesisDiggity_yr'+yr+'_ace2.npz'
#
# Mu-Ting followed Wheeler and Hendon, 2004 in computing the RMM values.  This involves the 
# removal of quite a bit of large-scale variability and I am still confused about how it is done in
# Wheeler and Hendon, as well as in Mu-Ting's code.  
#
# Needs to be removed: 
#   seasonal cycle
#   annual cycle --> see code_for_analysis/C.TC_genesis/C4.2_Calc_TCGI_anomaly.py
#   diurnal cycle
#   ENSO signal  --> not sure if or how this is being removed...
#
#  Is the calculation of anomalies in the context of TCGI the same as those used to compute RMM
#    indices? 
#
#  In C4.2_Calc_TCGI_anomaly.py it looks like this is Mu-Tings process: 
#    removed diurnal cycle to create V_ano
#    detrend with signal.detrend to create V_ano2  --> what is signal.detrend?
#    remove annual cycle with MJO.remove_anncycle_4d (or 3d) to create V_ano_final
#        remove_anncycle_#d seems to 'remove mean and first 3 harmonics'
#    transform the final variable to an xarray data array: V_ano_final = xr.DataArray(...)
#
# levi silvers
####################################################################################################

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.ndimage import uniform_filter1d
import sys
from scipy import signal
import os
import cartopy.util as cartopy_util
import cartopy.crs as ccrs
from datetime import datetime, timezone

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# test io 
if len(sys.argv) > 1:
    user_input = sys.argv[1]
    print(f"scumstash says, {user_input}...")
    ploc = sys.argv[1]
    print("we need the year, the decade, and the ensemble number to specify which of the 120 years we look at")
    yr = sys.argv[2]
    print(f"scumstash says, the tcSeason is: {yr}...")
    dstr = sys.argv[3]
    print(f"scumstash says, the decade in use is: {dstr}...")
    ensnum = sys.argv[4]
    print(f"scumstash says, the ensnum in use is: {ensnum}...")

dirstr    = '/home/lsilvers/'

if ploc == "luft": # paths for luft
  dirstr2   = '/Users/C823281551/'
  fig_dir_ace2 = dirstr2 + 'figures/ace2_fig/MJO/'
  file_dir3 = dirstr2 + 'data/ACE2/'
  file_dir2 = file_dir3
  sys.path.append('/Users/C823281551/code/pythonCode/TC_genesis_ACE2_evaluation_public/function/')
else: # default paths are for maui
  dirstr2   = '/bell-scratch/C823281551/'
  file_dir3 = dirstr + 'data/ACE2/'
  file_dir2 = dirstr2 + 'ACE2/testout/'
  fig_dir_ace2 = dirstr2 + 'figure/ace2_fig/MJO/'
  sys.path.append('/home/C823281551/code/pythonCode/TC_genesis_ACE2_evaluation_public/function/')

import mjo_mean_state_diagnostics_uw as MJO


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
yr_str    = '1'
tcSeason  = yr
DIR       = dirstr + 'code/pythonCode/ACE2/'
#
file_dir  = dirstr2 + 'data/ACE2/'
#
file_dir_era5_eof = dirstr2 + 'data/ACE2/'
file_dir_out = file_dir_era5_eof
filstr    = '_'+yr+'_'+dstr+'_'+ensnum+'_'
file1     = 'int_prec'+filstr+'b.nc'
file2     = 'int_'+yr+'_'+dstr+'_'+ensnum+'_u850_b.nc'
file3     = 'int_'+yr+'_'+dstr+'_'+ensnum+'_u200_b.nc'
ds        = xr.open_dataset(file_dir + file1, decode_timedelta=True)
print("original p data: ")
print(ds)
ds2       = xr.open_dataset(file_dir + file2, decode_timedelta=True)
ds3       = xr.open_dataset(file_dir + file3, decode_timedelta=True)
#

print("time is: ",ds.time.data)
print("attributes of ds are: ",ds.attrs) # it looks like the attributes of ds are an empty set
print("attributes of ds2 are: ",ds2.attrs) # it looks like the attributes of ds are an empty set
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('~~~~~~~~~~~~~~~~~~~New~Wave~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('incoming precipitation file is: ',file_dir + file1)
print('incoming wind file is: ',file_dir + file2)
print('file dir out is: ',file_dir_out)
print('~~~~~~~~~~~~~~~~~~~New~Wave~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## test for 1 year
endtime = 1460 # 1 year
#tc_genesis_file='/bell-scratch/C823281551/ACE2/testout/TC_genesis_1yr2003.0_ace2.npz'
tmpyr = '20'+ensnum 
yrint = int(tmpyr)
tc_genesis_file=file_dir2 + 'TC_genesis_1yr_'+yr+'_'+dstr+'_20'+ensnum+'.0_ace2.npz'

mem      = ds['sample']
lat_15SN = ds2['lat'][:]
lat      = ds2['lat']
lon      = ds2['lon']
temptime = ds2['time']
time     = temptime[0:endtime]
print('shape of time array is: ',np.shape(time))

nt       = np.size(time)
nlat     = np.size(lat_15SN)
nlon     = np.size(lon)
nmem     = np.size(mem)
dt       = 4 # how many data points per day
nday     = int(endtime/dt)
nt       = endtime

print('number of lats is: ',np.size(lat))
print('number of times is: ',np.size(time))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lat_15S = ds.lat.sel(lat=-15, method="nearest")
lat_15N = ds.lat.sel(lat=15, method="nearest")

u850a  = ds2['eastward_wind'][0:endtime,:,:]
u200a  = ds3['eastward_wind'][0:endtime,:,:]
PRECIP = ds['PRATEsfc'][0,0:endtime,:,:]
V    = PRECIP.transpose("time","lat","lon").values
u850 = u850a.transpose("time","lat","lon").values
u200 = u200a.transpose("time","lat","lon").values

print('shape of V is: ',np.shape(V))
print('shape of u850 is: ',np.shape(u850))
print('shape of u200 is: ',np.shape(u200))

V_reshape    = np.reshape(V, (nday, dt, nlat, nlon))
u850_reshape = np.reshape(u850, (nday, dt, nlat, nlon))
u200_reshape = np.reshape(u200, (nday, dt, nlat, nlon))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# calculate diurnal cycle to remove it

# numpy.tile constructs a new array by repeating an input array a specified number of times along each dimension
diurnal_cyc      = np.tile(np.nanmean(V_reshape,0).squeeze(), (nday,1,1,1))  # Mu-Ting had (nday,1,1,1,1)
#diurnal_cyc_flat = np.reshape(diurnal_cyc, (nday*dt, nlat, nlon, nmem))
diurnal_cyc_flat = np.reshape(diurnal_cyc, (nday*dt, nlat, nlon))
pre_ano     = V - diurnal_cyc_flat
# remove annual cycle
pre_ano2 = np.where(np.isnan(pre_ano)==1, -10**10, pre_ano)
pre_ano_final, cyc_final = MJO.remove_anncycle_3d( signal.detrend(pre_ano2, 0), time, lat, lon, 1/dt)
pre_ano_final = np.where(np.isnan(pre_ano.squeeze())==1, np.nan, pre_ano_final)
del pre_ano
#
prec_ano    = np.array(pre_ano_final).squeeze()
pr_ano       = xr.DataArray(prec_ano, dims=("time", "lat", "lon"))
#print('shape of pr_ano is: ',np.shape(pr_ano))

diurnal_cyc      = np.tile(np.nanmean(u850_reshape,0).squeeze(), (nday,1,1,1))  # Mu-Ting had (nday,1,1,1,1)
diurnal_cyc_flat = np.reshape(diurnal_cyc, (nday*dt, nlat, nlon))
u_850_ano            = u850 - diurnal_cyc_flat
# remove annual cycle
u_850_ano2 = np.where(np.isnan(u_850_ano)==1, -10**10, u_850_ano)
u_850_ano_final, cyc_final = MJO.remove_anncycle_3d( signal.detrend(u_850_ano2, 0), time, lat, lon, 1/dt)
u_850_ano_final = np.where(np.isnan(u_850_ano.squeeze())==1, np.nan, u_850_ano_final)
del u_850_ano
#
u1_ano           = np.array(u_850_ano_final).squeeze()
u850_ano         = xr.DataArray(u1_ano, dims=("time", "lat", "lon"))
#print('shape of u850_ano is: ',np.shape(u850_ano))

diurnal_cyc      = np.tile(np.nanmean(u200_reshape,0).squeeze(), (nday,1,1,1))  # Mu-Ting had (nday,1,1,1,1)
diurnal_cyc_flat = np.reshape(diurnal_cyc, (nday*dt, nlat, nlon))
u_200_ano            = u200 - diurnal_cyc_flat
# remove annual cycle
u_200_ano2 = np.where(np.isnan(u_200_ano)==1, -10**10, u_200_ano)
u_200_ano_final, cyc_final = MJO.remove_anncycle_3d( signal.detrend(u_200_ano2, 0), time, lat, lon, 1/dt)
u_200_ano_final = np.where(np.isnan(u_200_ano.squeeze())==1, np.nan, u_200_ano_final)
del u_200_ano
#
u1_ano           = np.array(u_200_ano_final).squeeze()
u200_ano         = xr.DataArray(u1_ano, dims=("time", "lat", "lon"))
#print('shape of u850_ano is: ',np.shape(u200_ano))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# calculate meridional average
# Calculate the meridional average of the precipitation
lat_radians = np.deg2rad(lat) 
weights     = np.cos(lat_radians)
pr_15SN_ano = (pr_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(pr_ano)).sum(dim="lat", skipna=True)
u850_15SN_ano = (u850_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(u850_ano)).sum(dim="lat", skipna=True)
u200_15SN_ano = (u200_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(u200_ano)).sum(dim="lat", skipna=True)
print("shape of pr_15SN_ano is: ",np.shape(pr_15SN_ano))   
print("shape of u850_15SN_ano is: ",np.shape(u850_15SN_ano))
print("shape of u200_15SN_ano is: ",np.shape(u200_15SN_ano))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# calculate 120 day running mean  

## remove the 120 day running mean to get subseasonal variability 
running_mean = uniform_filter1d(pr_ano, size=120*4, axis=0, mode='nearest')
pr_ano_final = pr_ano - running_mean
running_mean = uniform_filter1d(u850_ano, size=120*4, axis=0, mode='nearest')
u850_ano_final = u850_ano - running_mean
running_mean = uniform_filter1d(u200_ano, size=120*4, axis=0, mode='nearest')
u200_ano_final = u200_ano - running_mean

# remove the 120 day running mean from the meridionally averaged data: 
running_mean = uniform_filter1d(pr_15SN_ano, size=120*4, axis=0, mode='nearest')
pr_15SN_ano_highpass = pr_15SN_ano - running_mean
# deal with nans at longitude of 0
pr_15SN_ano_highpass[:,0] = ( pr_15SN_ano_highpass[:,1].values + pr_15SN_ano_highpass[:,-1].values )/2
#
running_mean = uniform_filter1d(u850_15SN_ano, size=120*4, axis=0, mode='nearest')
u850_15SN_ano_highpass = u850_15SN_ano - running_mean
u850_15SN_ano_highpass[:,0] = ( u850_15SN_ano_highpass[:,1].values + u850_15SN_ano_highpass[:,-1].values )/2
#
running_mean = uniform_filter1d(u200_15SN_ano, size=120*4, axis=0, mode='nearest')
u200_15SN_ano_highpass = u200_15SN_ano - running_mean
u200_15SN_ano_highpass[:,0] = ( u200_15SN_ano_highpass[:,1].values + u200_15SN_ano_highpass[:,-1].values )/2


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pr_final   = pr_15SN_ano_highpass.values
u850_final = u850_15SN_ano_highpass.values
u200_final = u200_15SN_ano_highpass.values

# find nans
print(np.sum(np.isnan(pr_final)))
print(np.sum(np.isnan(u850_final)))
print(np.sum(np.isnan(u200_final)))

print(np.shape(pr_final))
print(np.shape(u850_final))
print(np.shape(u200_final))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use EOF from ERA5 to construct the RMM index in ACE2

X, mu_u850, std_u850, mu_u200, std_u200, mu_pr, std_pr = MJO.normalize_before_ceof(u850_final,u200_final, pr_final)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use pr, u200, u850 to construct RMM index. 
# EOF Analysis
data = np.load(file_dir3 + 'MJO_EOF_ERA5_2001_2010.npz')
EOF  = data['EOF']
print('ERA5 EOF file is: ',file_dir3+'MJO_EOF_ERA5_2001_2010.npz')

# Get PCs by projecting onto observed EOF
PC = np.dot(EOF, X)

X_u850 = X[0:nlon,:]
X_u200 = X[nlon:2*nlon,:]
X_olr  = X[2*nlon:3*nlon,:]
EOF_u850 = EOF[:,0:nlon]
EOF_u200 = EOF[:,nlon:2*nlon]
EOF_pr  = EOF[:,2*nlon:3*nlon]
PC_u850 = np.matmul(EOF_u850,X_u850)
PC_u200 = np.matmul(EOF_u200,X_u200)
PC_pr = np.matmul(EOF_pr,X_olr)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
model_name = 'ACE2'+'-'+yr

# plot pc lag-regression
calc_rmm = 1

if calc_rmm == 1:
    rmm1 = PC[0] #or -PC[0]. you may want to check this by doing the phase composite (this could also be negative) (Check if each phase corresponds to the correct enhanced convection region)!
    rmm2 = PC[1] #or -PC[1]. you may want to check this by doing the phase composite (this could also be negative)!
    rmm1_u850 = PC_u850[0]
    rmm2_u850 = PC_u850[1]
    rmm1_u200 = PC_u200[0]
    rmm2_u200 = PC_u200[1]
    rmm1_pr  = PC_pr[0]
    rmm2_pr  = PC_pr[1]

    output = file_dir_out+'RMM_PC_ACE2_2001_2010.npz'
    np.savez(output, X=X,EOF=EOF,PC=PC,rmm1=rmm1,rmm2=rmm2,\
                rmm1_u850=rmm1_u850, rmm2_u850=rmm2_u850,\
                rmm1_u200=rmm1_u200, rmm2_u200=rmm2_u200,\
                rmm1_pr =rmm1_pr,  rmm2_pr=rmm2_pr)
else:
    data = np.load(file_dir_out+'RMM_PC_ACE2_2001_2010.npz')
    rmm1 = data['rmm1']
    rmm2 = data['rmm2']


lag = 25*4

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('shape and size of rmm1 and rmm2 are: ',np.shape(rmm1),' and ',np.size(rmm1))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('shape and size of rmm1 and rmm2_u850 are: ',np.shape(rmm1_u850),' and ',np.size(rmm1_u850))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('shape and size of rmm1 and rmm2 are: ',np.shape(rmm1_pr),' and ',np.size(rmm1_pr))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

cor_11 = np.zeros([2*lag+1])
cor_21 = np.zeros([2*lag+1])
for i in range(1,lag+1):
    k = lag+1-i
    temp = np.corrcoef( rmm1[0:nt-k], rmm1[k:nt] ) 
    cor_11[i-1] = temp[0,1]
    temp = np.corrcoef( rmm2[0:nt-k], rmm1[k:nt] )
    cor_21[i-1] = temp[0,1]
    temp = np.corrcoef( rmm1[0:nt-i+1],rmm1[i-1:nt] ) 
    cor_11[lag+i-1] = temp[0,1]
    temp = np.corrcoef( rmm1[0:nt-i+1],rmm2[i-1:nt] )
    cor_21[lag+i-1] = temp[0,1]
temp = np.corrcoef( rmm1[0:nt-lag],rmm1[lag:nt] )
cor_11[2*lag] = temp[0,1]
temp = np.corrcoef( rmm1[0:nt-lag],rmm2[lag:nt] )
cor_21[2*lag] = temp[0,1]
LAG = np.arange(-lag,lag+1)

zero = np.zeros([2*lag+1])
fig = plt.figure(figsize=(12, 9))
plt.rcParams.update({'font.size': 20})
plt.grid(True, linestyle='-.')
plt.plot(LAG/4,cor_11,'b',LAG/4,cor_21,'r',LAG/4,zero,'k')
plt.xlim([-25,25])
plt.xticks([-25,-20,-10,0,10,20,25])
plt.xlabel('lag (days)')
plt.ylabel('corr coefficient')
plt.legend(('RMM1&1','RMM1&2'))
plt.title(model_name+' PC lagcorr')
#plt.savefig(fig_dir_ace2+'WH'+filstr+'pc_lagcorr.png')
#plt.show()
#print('output figures here: ',fig_dir_ace2)

def plot_rmm_timeseries(time, rmm1_norm, rmm2_norm, fig_dir_ace2, filstr):
    """
    Function to plot the RMM time series, excluding first and last times, and shading regions based on 8 MJO phases with pastel colors.
    """
    golden_ratio = (1 + 5**0.5) / 2
    fig = plt.figure(figsize=(12, 12 / golden_ratio))
    plt.rcParams.update({'font.size': 18})
    #plt.legend(('850 wind','200 wind','Precipitation'))
    #plt.plot(time[:],rmm1_norm[:],'k')
    #plt.plot(time[:],rmm2_norm[:],'r')
    #plt.xlabel('time')
    plt.ylabel('rmm1 norm magnitude')

    # Format x-axis to show months
    #plt.xticks(rotation=45)
    days = time.dt.days
    # Smooth the time series with 5-point running mean
    rmm1_smooth = uniform_filter1d(rmm1_norm, size=9, mode='nearest')
    rmm2_smooth = uniform_filter1d(rmm2_norm, size=9, mode='nearest')
    # Exclude first and last times
    plt.plot(days[1:-1], rmm1_smooth[1:-1], 'k')
    plt.plot(days[1:-1], rmm2_smooth[1:-1], '--k')
    # plt.xlabel('days since start')
    
    # Compute MJO phases
    # TAG marker 1
    phase = np.full_like(rmm1_norm, np.nan)
    for it in range(len(rmm1_norm)):
        RMM1_tmp = rmm1_norm[it]
        RMM2_tmp = rmm2_norm[it]
        A = RMM1_tmp**2 + RMM2_tmp**2
        if A < 1:
           # continue
           phase[it] = 9
        if RMM1_tmp < 0 and RMM2_tmp < 0:
            if np.abs(RMM1_tmp) > np.abs(RMM2_tmp):
                phase[it] = 1
            else:
                phase[it] = 2
        elif RMM1_tmp > 0 and RMM2_tmp < 0:
            if np.abs(RMM1_tmp) < np.abs(RMM2_tmp):
                phase[it] = 3
            else:
                phase[it] = 4
        elif RMM1_tmp > 0 and RMM2_tmp > 0:
            if np.abs(RMM1_tmp) > np.abs(RMM2_tmp):
                phase[it] = 5
            else:
                phase[it] = 6
        elif RMM1_tmp < 0 and RMM2_tmp > 0:
            if np.abs(RMM1_tmp) < np.abs(RMM2_tmp):
                phase[it] = 7
            else:
                phase[it] = 8
    
    # Calculate percentage of time in phases 1,2,3,8 with |RMM| >1 between June 1 and November 30
    #mask_period = (time.dt.days > 151) & (time.dt.days <= 334)
    mask_period = (time.dt.days > 211) & (time.dt.days <= 273)  # --> August through September
    mask_phase = np.isin(phase, [1, 2, 3])
    mask_rmm = (np.abs(rmm1_norm) > 1) | (np.abs(rmm2_norm) > 1)
    combined_mask = mask_phase & mask_rmm & mask_period
    percentage = np.sum(combined_mask) / np.sum(mask_period) * 100
    print(f"Percentage of time in phases 1,2,3,8 with |RMM| > 1 between June 1 and November 30: {percentage:.2f}%")
    
    # Pastel colors for 8 phases (stronger contrast for used phases)
    pastel_colors = ['#FF0000', '#FFA500', '#FFFF00', '#BAFFBA', '#BAE1FF', '#D1BAFF', '#FFB3D1', '#800080']
    
    # Shade regions for each phase, only where |RMM| >1

    for i in [1, 2, 3, 8]:
    #for i in [1, 2, 3]:
        # For rmm1_norm positive
        mask_pos1 = (rmm1_smooth > 1) & (phase == i)
        plt.fill_between(days[1:-1], 1, rmm1_smooth[1:-1], where=mask_pos1[1:-1], color=pastel_colors[i-1], alpha=0.5)
        # For rmm1_norm negative
        mask_neg1 = (rmm1_smooth < -1) & (phase == i)
        plt.fill_between(days[1:-1], -1, rmm1_smooth[1:-1], where=mask_neg1[1:-1], color=pastel_colors[i-1], alpha=0.5)
        # For rmm2_norm positive
        mask_pos2 = (rmm2_smooth > 1) & (phase == i)
        plt.fill_between(days[1:-1], 1, rmm2_smooth[1:-1], where=mask_pos2[1:-1], color=pastel_colors[i-1], alpha=0.5)
        # For rmm2_norm negative
        mask_neg2 = (rmm2_smooth < -1) & (phase == i)
        plt.fill_between(days[1:-1], -1, rmm2_smooth[1:-1], where=mask_neg2[1:-1], color=pastel_colors[i-1], alpha=0.5)
    
    # Set monthly markers assuming day 1 (day 0 in array) is January 1st
    month_starts = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    month_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    plt.xticks(month_starts, month_labels)
    plt.xlabel('Month')
    
    # Add legend for time series and phases
    line1 = Line2D([0], [0], color='k', label='RMM 1')
    line2 = Line2D([0], [0], color='k', linestyle='dashed', label='RMM 2')
    phase_elements = [Patch(facecolor=pastel_colors[i-1], label=f'Phase {i}') for i in [1, 2, 3, 8]]
    all_handles = [line1, line2] + phase_elements
    plt.legend(handles=all_handles, loc='upper left')
    
    plt.savefig(fig_dir_ace2+'monkey'+filstr+'rmm_norm_ts.png', dpi=300)
    return percentage

'''
RMM 8 phase index
'''
time_val = time.values
n,RMM_ind,rmm1_norm,rmm2_norm = MJO.rmm_eight_phase_index(rmm1,rmm2,time,rmm1,rmm2)

valuep = plot_rmm_timeseries(time, rmm1_norm, rmm2_norm, fig_dir_ace2, filstr)


#plot 8 phase diagram
ma = 4.5 #max amplitude
z = np.zeros(4) #zero
h = np.array([1,2,3,ma]) #horizontal
TT = np.array([0.5**0.5,2,3,ma]) #tilt
dphi = 2*np.pi/30
phi = np.arange(0,2*np.pi+dphi,dphi)
cos = np.cos(phi) #weak mjo (circle) 
sin = np.sin(phi) #weak mjo (circle)
#
ndays2plot = 1825 
nd2pl = str(ndays2plot)
#
fig = plt.figure(figsize=(12, 12))
plt.rcParams.update({'font.size': 18})
plt.plot(rmm1_norm[0:ndays2plot*4:4],rmm2_norm[0:ndays2plot*4:4],'b-o',markersize=2)
plt.plot(rmm1_norm[0],rmm2_norm[0],'k*')
plt.plot(-h,z,'k',h,z,'k',z,h,'k',z,-h,'k',-TT,TT,'k',-TT,-TT,'k',TT,-TT,'k',TT,TT,'k',cos,sin,'k')
plt.xlabel('RMM1')
plt.ylabel('RMM2')
plt.title('MJO from 1 ensemble: '+filstr)
plt.axis([-ma,ma,-ma,ma])
plt.savefig(fig_dir_ace2+'WH'+filstr+'pc_phasediag.png')
#plt.savefig(fig_dir_ace2+model_name+dstr+'phase_diagram_day0-'+nd2pl+'.png')
#plt.savefig(fig_dir_ace2+dstr+'phase_diagram.png')
#plt.show()

print('finish plotting rmm lag corr, phase diagram')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('shape and size of rmm1_norm and rmm2_norm are: ',np.shape(rmm1_norm),' and ',np.size(rmm1_norm))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## MJO-8 phase composite
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
Use RMM-8 phase index for composite
Make sure : time period of the compositing variable = time period of eof variables!!!
Otherwise, you need to change the time period.
'''

model_name = 'ACE2'
vname = list(['pr','u850','u200'])

composite_8ph = 1
if composite_8ph == 1:

    for v in range(0, np.size(vname)):

        n,RMM_ind,rmm1_norm,rmm2_norm = MJO.rmm_eight_phase_index(rmm1,rmm2,time,rmm1,rmm2)

        VAR = globals()[vname[v]+'_ano_final'] #(time, lat, lon)

        if v == 0:
            pr_8ph   = MJO.eight_phase_composite(VAR[:,:,:],RMM_ind)
        elif v == 1:
            u850_8ph = MJO.eight_phase_composite(VAR[:,:,:],RMM_ind)
        elif v == 2:
            u200_8ph = MJO.eight_phase_composite(VAR[:,:,:],RMM_ind)


    pr_8ph_rms   = np.sqrt(pr_8ph[:,:,:]**2)
    u850_8ph_rms = np.sqrt(u850_8ph[:,:,:]**2)
    u200_8ph_rms = np.sqrt(u200_8ph[:,:,:]**2)



    # Save output (this is what we should eventually open in a new scripts, along with other ensemble members of choice, and then
    # plot average fields for a particular year, or for a particular set of ensemble numbers...)
    output2 = file_dir_out+'MJO_8ph_composite_ACE2'+filstr+'1yr.npz'
    np.savez(output2, u850_8ph = u850_8ph, u200_8ph = u200_8ph, pr_8ph = pr_8ph, \
                    RMM_ind = RMM_ind,
                    pr_8ph_rms = pr_8ph_rms, u850_8ph_rms = u850_8ph_rms, u200_8ph_rms = u200_8ph_rms, \
                    time = time, lon = lon, lat = lat)

else:
    data     = np.load(file_dir_out+'MJO_8ph_composite_ACE2_2001_2010.npz')
    RMM_ind  = data['RMM_ind']
    u850_8ph = data['u850_8ph']
    u200_8ph = data['u200_8ph']
    pr_8ph   = data['pr_8ph']

print('finish saving 8phase-composite data')

'''
Plot rmm 8-phases composite: olr, u850, u200
'''

vname_long = list(['precipitation (mm/day)','u850 (m/s)','u200 (m/s)'])
vname = list(['pr','u850','u200'])
model_name = 'ERA5'
cmap_list = list(['RdBu','RdBu_r','RdBu_r'])

# Set Contour Level
clev1 = np.arange(-5,5.5,0.5) # pr
cticks1 = np.arange(-5,6,1)
clev2 = np.arange(-5,5.5,0.5) # u850
cticks2 = np.arange(-5,6,1)
clev3 = np.arange(-10, 11, 1) # u200
cticks3 = np.arange(-10, 12, 2)

print('save output figure to: /bell-scratch/C823281551/figure/ace2_fig/MJO/ ')

for v in range(0,3):#np.size(vname)):
    v_in = globals()[vname[v]+'_8ph']
    clev = globals()['clev'+str(v+1)]
    cticks = globals()['cticks'+str(v+1)]
    if v == 0: #moisture/pr (blue positive, red negative)
        cbar = "RdBu"
    else:
        cbar = "RdBu_r"

    if v == 0:
        scalef = 86400.
    else:
        scalef = 1.

    #fig_name = 'Fig.1_MJO_8phase_composite_'+yr+dstr+'_'+vname[v]+'.png'
    fig_name = 'Fig_8phase_ghosts'+filstr+vname[v]+'.png'

    fig, axes = plt.subplots(8,1,figsize=(6.5, 7),dpi=600, subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)} )
    plt.subplots_adjust(left=0.1, right=0.98,top=0.9,bottom=0.15,hspace=0.9, wspace=0.1)
    plt.rcParams.update({'font.size': 7})

    for iplt in range(0,8): # Each phase
        plt.subplot(8,1, iplt+1)
        ax = plt.gca()

        V_tmp = v_in[iplt,:,:]
        lon_tmp = lon
        lat_tmp = lat

        #print(lon_tmp)
        [xx, yy] = np.meshgrid(lon_tmp, lat_tmp)

        # Handle the data to prevent white line
        [V_tmp_cyclic, lon_cyclic] = cartopy_util.add_cyclic_point(
            V_tmp.T,
            coord=lon_tmp,
            axis=0
        )

        ax.coastlines(color='grey', linewidth=0.75)
        ax.set_xticks(np.arange(0,360,60), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(-10,20,10), crs=ccrs.PlateCarree())
        ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W'], fontsize=6)
        ax.set_yticklabels(['10S', '0', '10N'], fontsize=6)

        # Plot the data
        contour = plt.contourf(
            lon_cyclic, lat_tmp, scalef*V_tmp_cyclic.T, cmap=cmap_list[v],
            transform=ccrs.PlateCarree(), levels= clev, extend='both'
        )

        ax.set_title('Phase '+str(iplt+1), pad=1,loc='right',fontsize=7)

    plt.suptitle('MJO composite '+vname_long[v]+' (ACE2, 1yr)', y=0.96)

    cb = fig.colorbar(contour, ax=axes[:], orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.05, aspect=40)
    cb.ax.tick_params(labelsize=6)
    cb.set_ticks(cticks)
    plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    #plt.savefig(fig_dir_ace2+model_name+'phase_diagram_day0-100.png')
    #plt.show()
    plt.close()


# Find TC genesis, composited by MJO phase

####################
# Function 1 to convert timestamp to hours since Unix epoch
#def timestamp_to_hours_since_epoch(timestamp_str, yr_start=2003):
def timestamp_to_hours_since_epoch(timestamp_str, yr_start=yrint):
    # Parse the timestamp up to seconds
    datetime_obj = datetime.strptime(timestamp_str[:19], '%Y-%m-%dT%H:%M:%S')
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)

    # Define the Unix epoch
    epoch = datetime(yr_start, 1, 1, tzinfo=timezone.utc)

    # Calculate the difference in hours
    hours_since_epoch = (datetime_obj - epoch).total_seconds() / 3600
    return hours_since_epoch

#######################
# Function 2 to convert timestamp to hours since Unix epoch
def timestamp_to_hours_since_epoch2(timestamp, yr_start=yrint):

    # Convert numpy.datetime64 to a Python datetime object
    if isinstance(timestamp, np.datetime64):
        datetime_obj = timestamp.astype('datetime64[s]').tolist()
    else:
        return None  # Handle the case if the object is not a valid datetime64 instance

    # Convert to UTC timezone
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)

    # Define the Unix epoch
    epoch = datetime(yr_start, 1, 1, tzinfo=timezone.utc)

    # Calculate the difference in hours
    hours_since_epoch = (datetime_obj - epoch).total_seconds() / 3600
    return hours_since_epoch

#######################
# Find the 8-phase info for each time (Copied from function:rmm_eight_phase_index!)
MJO_phase_timeseries = np.empty([np.size(time)])
MJO_phase_timeseries[:] = np.nan

for it in range(0, np.size(time)):

    RMM1_tmp = rmm1_norm[it]
    RMM2_tmp = rmm2_norm[it]
    # TAG marker 2
    A = RMM1_tmp**2 + RMM2_tmp**2
    if (A<1).any(): #weak MJO
        #MJO_phase_timeseries[it] = np.nan
        MJO_phase_timeseries[it] = 9 # this defines events with weak or zero MJO
    elif RMM1_tmp<0 and RMM2_tmp<0 and np.abs(RMM1_tmp)>np.abs(RMM2_tmp): #PHASE1
        MJO_phase_timeseries[it] = 1
    elif RMM1_tmp<0 and RMM2_tmp<0 and np.abs(RMM1_tmp)<np.abs(RMM2_tmp): #2
        MJO_phase_timeseries[it] = 2
    elif RMM1_tmp>0 and RMM2_tmp<0 and np.abs(RMM1_tmp)<np.abs(RMM2_tmp): #3 
        MJO_phase_timeseries[it] = 3
    elif RMM1_tmp>0 and RMM2_tmp<0 and np.abs(RMM1_tmp)>np.abs(RMM2_tmp): #4
        MJO_phase_timeseries[it] = 4
    elif RMM1_tmp>0 and RMM2_tmp>0 and np.abs(RMM1_tmp)>np.abs(RMM2_tmp): #5
        MJO_phase_timeseries[it] = 5
    elif RMM1_tmp>0 and RMM2_tmp>0 and np.abs(RMM1_tmp)<np.abs(RMM2_tmp): #6
        MJO_phase_timeseries[it] = 6
    elif RMM1_tmp<0 and RMM2_tmp>0 and np.abs(RMM1_tmp)<np.abs(RMM2_tmp): #7
        MJO_phase_timeseries[it] = 7
    elif RMM1_tmp<0 and RMM2_tmp>0 and np.abs(RMM1_tmp)>np.abs(RMM2_tmp): #8
        MJO_phase_timeseries[it] = 8 

####
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(MJO_phase_timeseries)
print('size and shape of MJO_phase_timeseries is: ',np.size(MJO_phase_timeseries),' and ',np.shape(MJO_phase_timeseries))
print('sum of nans in MJO_phase_timeseries',np.sum(np.isnan(MJO_phase_timeseries)))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

fig = plt.figure(figsize=(12, 12))
plt.rcParams.update({'font.size': 18})
plt.hist(MJO_phase_timeseries, bins=20)
#plt.hist(rmm2_norm)
#plt.plot(rmm1_norm[0:ndays2plot*4:4],rmm2_norm[0:ndays2plot*4:4],'b-o',markersize=4)
#plt.plot(rmm1_norm[0],rmm2_norm[0],'k*')
#plt.plot(-h,z,'k',h,z,'k',z,h,'k',z,-h,'k',-TT,TT,'k',-TT,-TT,'k',TT,-TT,'k',TT,TT,'k',cos,sin,'k')
#plt.xlabel('RMM1')
#plt.ylabel('RMM2')
#plt.axis([-ma,ma,-ma,ma])
plt.ylim(0, 170)
plt.savefig(fig_dir_ace2+'MJOhist'+filstr+'pc_phasediag.png')
#plt.savefig(dir_out+'/figure/ceof_rmm/'+model_name+'phase_diagram_day0-100.png')
plt.show()

###########
# Load TC genesis data
latmax = 30

# Load TC genesis event between 30S-30N
# generated with tc_numPerYear_ace2.py script
data = np.load(tc_genesis_file)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('WARNING!! are you using the correct TC geneis file? ',tc_genesis_file)
print('incoming files are from simulations of ',yr)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
lon_TC = data['lon_TC']
lat_TC = data['lat_TC']
yr_TC  = data['yr']
mon_TC = data['mon']
day_TC = data['day']
hr_TC  = data['hr']

# Transform time data in TC into the same format as time_phase_ace2

# Import numpy arrays of date information from TC, convert to int
yr = yr_TC.astype(int)
mon = mon_TC.astype(int)
day = day_TC.astype(int)
hr = hr_TC.astype(int)

# Create an empty list to store datetime strings
datetime_strings_TC = []

# Loop through the arrays to format as ISO 8601 strings
for y, m, d, h in zip(yr, mon, day, hr):
    dt = datetime(y, m, d, h)  # Create a datetime object
    datetime_strings_TC.append(dt.strftime('%Y-%m-%dT%H:%M:%S'))  # Format as ISO 8601

# Convert to hours since 2001-01-01:00
hours_since_2001_TC = [timestamp_to_hours_since_epoch(ts) for ts in datetime_strings_TC] 

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#t1 = 340
#t2 = 350
t1 = 20
t2 = 300
#print('shape of hours_since_2001_TC:',np.shape(hours_since_2001_TC))
print('MJO_phase_timeseries: ',MJO_phase_timeseries[0:t2])
print('first hours since TC: ',hours_since_2001_TC[0:30])
print('hours since TC: ',hours_since_2001_TC[t1:t2])
print('shape of hours_since_2001_TC:',np.shape(hours_since_2001_TC))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

###########
# Transform time data from MJO
# note that hours_since_2001_MJO is just an array of regularly increasing integers. 
hours_since_2001_MJO = np.arange(6, 6*np.size(time)+6, 6) 
print('first hours since 2001 MJO: ',hours_since_2001_MJO[0:20])
print('hours since 2001 MJO: ',hours_since_2001_MJO[t1:t2])
print('shape of hours_since_2001_MJO:',np.shape(hours_since_2001_MJO))
#dates = datetime(hours_since_2001_MJO)
#print('test of datetime: ',dates)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# Find the MJO phase for each TC genesis event
TC_MJO_phase = np.empty([np.size(lon_TC)])
print('shape of TC_MJO_phase',np.shape(TC_MJO_phase))
print('shape of MJO_phase_timeseries',np.shape(MJO_phase_timeseries))
print('size of lon_TC is: ',np.size(lon_TC))
for i in range(0, np.size(lon_TC)):
    if any(hours_since_2001_MJO == hours_since_2001_TC[i]):
        it = np.argwhere(hours_since_2001_MJO == hours_since_2001_TC[i]).squeeze()
        #print('value of i is: ',i,'value of it is: ',it,' value of MJO_phase_timeseries is: ',MJO_phase_timeseries[it])
        TC_MJO_phase[i] = MJO_phase_timeseries[it]
    else:
        print('value of i is: ',i,'value of it is: ',it)
        print('apparently no TCs formed during the MJO in this ensemble member.  weird.')

###########
## Save TC genesis data for each MJO phase
#
# TAG marker 3
save_lon_lat_genesis = 1 

if save_lon_lat_genesis == 1:
    lon_TC_phase1 = np.where(TC_MJO_phase==1, lon_TC, np.nan)
    lat_TC_phase1 = np.where(TC_MJO_phase==1, lat_TC, np.nan)
    lon_TC_phase1 = lon_TC_phase1[~np.isnan(lon_TC_phase1)]
    lat_TC_phase1 = lat_TC_phase1[~np.isnan(lat_TC_phase1)]
    #
    lon_TC_phase2 = np.where(TC_MJO_phase==2, lon_TC, np.nan)
    lat_TC_phase2 = np.where(TC_MJO_phase==2, lat_TC, np.nan)
    lon_TC_phase2 = lon_TC_phase2[~np.isnan(lon_TC_phase2)]
    lat_TC_phase2 = lat_TC_phase2[~np.isnan(lat_TC_phase2)]
    #
    lon_TC_phase3 = np.where(TC_MJO_phase==3, lon_TC, np.nan)
    lat_TC_phase3 = np.where(TC_MJO_phase==3, lat_TC, np.nan)
    lon_TC_phase3 = lon_TC_phase3[~np.isnan(lon_TC_phase3)]
    lat_TC_phase3 = lat_TC_phase3[~np.isnan(lat_TC_phase3)]
    #
    lon_TC_phase4 = np.where(TC_MJO_phase==4, lon_TC, np.nan)
    lat_TC_phase4 = np.where(TC_MJO_phase==4, lat_TC, np.nan)
    lon_TC_phase4 = lon_TC_phase4[~np.isnan(lon_TC_phase4)]
    lat_TC_phase4 = lat_TC_phase4[~np.isnan(lat_TC_phase4)]
    #
    lon_TC_phase5 = np.where(TC_MJO_phase==5, lon_TC, np.nan)
    lat_TC_phase5 = np.where(TC_MJO_phase==5, lat_TC, np.nan)
    lon_TC_phase5 = lon_TC_phase5[~np.isnan(lon_TC_phase5)]
    lat_TC_phase5 = lat_TC_phase5[~np.isnan(lat_TC_phase5)]
    #
    lon_TC_phase6 = np.where(TC_MJO_phase==6, lon_TC, np.nan)
    lat_TC_phase6 = np.where(TC_MJO_phase==6, lat_TC, np.nan)
    lon_TC_phase6 = lon_TC_phase6[~np.isnan(lon_TC_phase6)]
    lat_TC_phase6 = lat_TC_phase6[~np.isnan(lat_TC_phase6)]
    #
    lon_TC_phase7 = np.where(TC_MJO_phase==7, lon_TC, np.nan)
    lat_TC_phase7 = np.where(TC_MJO_phase==7, lat_TC, np.nan)
    lon_TC_phase7 = lon_TC_phase7[~np.isnan(lon_TC_phase7)]
    lat_TC_phase7 = lat_TC_phase7[~np.isnan(lat_TC_phase7)]
    #
    lon_TC_phase8 = np.where(TC_MJO_phase==8, lon_TC, np.nan)
    lat_TC_phase8 = np.where(TC_MJO_phase==8, lat_TC, np.nan)
    lon_TC_phase8 = lon_TC_phase8[~np.isnan(lon_TC_phase8)]
    lat_TC_phase8 = lat_TC_phase8[~np.isnan(lat_TC_phase8)]
    #
    lon_TC_phase9 = np.where(TC_MJO_phase==9, lon_TC, np.nan)
    lat_TC_phase9 = np.where(TC_MJO_phase==9, lat_TC, np.nan)
    lon_TC_phase9 = lon_TC_phase9[~np.isnan(lon_TC_phase9)]
    lat_TC_phase9 = lat_TC_phase9[~np.isnan(lat_TC_phase9)]


    output2 = file_dir_out+'TC_genesis_lon_lat_9phase_ACE2_1yr.npz'
    np.savez(output2, lon_TC_phase1=lon_TC_phase1, lat_TC_phase1=lat_TC_phase1,\
            lon_TC_phase2=lon_TC_phase2, lat_TC_phase2=lat_TC_phase2,\
            lon_TC_phase3=lon_TC_phase3, lat_TC_phase3=lat_TC_phase3,\
            lon_TC_phase4=lon_TC_phase4, lat_TC_phase4=lat_TC_phase4,\
            lon_TC_phase5=lon_TC_phase5, lat_TC_phase5=lat_TC_phase5,\
            lon_TC_phase6=lon_TC_phase6, lat_TC_phase6=lat_TC_phase6,\
            lon_TC_phase7=lon_TC_phase7, lat_TC_phase7=lat_TC_phase7,\
            lon_TC_phase8=lon_TC_phase8, lat_TC_phase8=lat_TC_phase8,\
            lon_TC_phase9=lon_TC_phase9, lat_TC_phase9=lat_TC_phase9)


else:
    data = np.load(file_dir_out+'TC_genesis_lon_lat_9phase_ACE2_1yr.npz')
    lon_TC_phase1 = data['lon_TC_phase1']
    lon_TC_phase2 = data['lon_TC_phase2']
    lon_TC_phase3 = data['lon_TC_phase3']
    lon_TC_phase4 = data['lon_TC_phase4']
    lon_TC_phase5 = data['lon_TC_phase5']
    lon_TC_phase6 = data['lon_TC_phase6']
    lon_TC_phase7 = data['lon_TC_phase7']
    lon_TC_phase8 = data['lon_TC_phase8']
    lon_TC_phase9 = data['lon_TC_phase9']
    #
    lat_TC_phase1 = data['lat_TC_phase1']
    lat_TC_phase2 = data['lat_TC_phase2']
    lat_TC_phase3 = data['lat_TC_phase3']
    lat_TC_phase4 = data['lat_TC_phase4']
    lat_TC_phase5 = data['lat_TC_phase5']
    lat_TC_phase6 = data['lat_TC_phase6']
    lat_TC_phase7 = data['lat_TC_phase7']
    lat_TC_phase8 = data['lat_TC_phase8']
    lat_TC_phase9 = data['lat_TC_phase9']

###########

# TAG marker 3 or 4?
save_mon_TC = 1
if save_mon_TC == 1:

    mon_TC_phase1 = np.where(TC_MJO_phase==1, mon_TC, np.nan)
    mon_TC_phase1 = mon_TC_phase1[~np.isnan(mon_TC_phase1)]
    #
    mon_TC_phase2 = np.where(TC_MJO_phase==2, mon_TC, np.nan)
    mon_TC_phase2 = mon_TC_phase2[~np.isnan(mon_TC_phase2)]
    #
    mon_TC_phase3 = np.where(TC_MJO_phase==3, mon_TC, np.nan)
    mon_TC_phase3 = mon_TC_phase3[~np.isnan(mon_TC_phase3)]
    #
    mon_TC_phase4 = np.where(TC_MJO_phase==4, mon_TC, np.nan)
    mon_TC_phase4 = mon_TC_phase4[~np.isnan(mon_TC_phase4)]
    #
    mon_TC_phase5 = np.where(TC_MJO_phase==5, mon_TC, np.nan)
    mon_TC_phase5 = mon_TC_phase5[~np.isnan(mon_TC_phase5)]
    #
    mon_TC_phase6 = np.where(TC_MJO_phase==6, mon_TC, np.nan)
    mon_TC_phase6 = mon_TC_phase6[~np.isnan(mon_TC_phase6)]
    #
    mon_TC_phase7 = np.where(TC_MJO_phase==7, mon_TC, np.nan)
    mon_TC_phase7 = mon_TC_phase7[~np.isnan(mon_TC_phase7)]
    #
    mon_TC_phase8 = np.where(TC_MJO_phase==8, mon_TC, np.nan)
    mon_TC_phase8 = mon_TC_phase8[~np.isnan(mon_TC_phase8)]
    #
    mon_TC_phase9 = np.where(TC_MJO_phase==9, mon_TC, np.nan)
    mon_TC_phase9 = mon_TC_phase9[~np.isnan(mon_TC_phase9)]

    output2 = file_dir_out+'TC_genesis_month_9phase_ACE2_1yr.npz'
    np.savez(output2, mon_TC_phase1=mon_TC_phase1,\
            mon_TC_phase2=mon_TC_phase2,\
            mon_TC_phase3=mon_TC_phase3,\
            mon_TC_phase4=mon_TC_phase4,\
            mon_TC_phase5=mon_TC_phase5,\
            mon_TC_phase6=mon_TC_phase6,\
            mon_TC_phase7=mon_TC_phase7,\
            mon_TC_phase8=mon_TC_phase8,\
            mon_TC_phase9=mon_TC_phase9)
else:
    data = np.load(file_dir_out+'TC_genesis_month_9phase_ACE2_1yr.npz')
    mon_TC_phase1 = data['mon_TC_phase1']
    mon_TC_phase2 = data['mon_TC_phase2']
    mon_TC_phase3 = data['mon_TC_phase3']
    mon_TC_phase4 = data['mon_TC_phase4']
    mon_TC_phase5 = data['mon_TC_phase5']
    mon_TC_phase6 = data['mon_TC_phase6']
    mon_TC_phase7 = data['mon_TC_phase7']
    mon_TC_phase8 = data['mon_TC_phase8']
    mon_TC_phase9 = data['mon_TC_phase9']

#################
# Calculate TC genesis number for each MJO phase for each basin

# Load basin info
basin_list    = list(['NI','NWPAC','NEPAC','NATL','SI','SPAC'])
basin_long_list = list(['North IO','North WestPac','North EastPac','North Atl','South IO','South Pac'])
basin_lon_min = np.array([45, 105, 180, 265, 35, 135])
basin_lon_max = np.array([105, 180, 265, 357.5, 135, 270])
latmax = 30 #25 is not used, use 30
basin_lat_min = np.array([0,    0,    0,  0,  -latmax, -latmax])
basin_lat_max = np.array([latmax,  latmax, latmax, latmax,    0, 0])
nbasin        = np.size(basin_list)

################
# TAG marker 5
calc_TC_genesis_phase_basin = 1

if calc_TC_genesis_phase_basin == 1:
    nphase = 9
    TC_genesis_MJO_phase_basin = np.zeros([nphase, nbasin])

    for iph in range(0, nphase):
        lon_tmp = globals()['lon_TC_phase'+str(iph+1)]
        lat_tmp = globals()['lat_TC_phase'+str(iph+1)]
        for i in range(0, np.size(lon_tmp)):
            for ibasin in range(0, nbasin):
                dlonmin = lon_tmp[i]-basin_lon_min[ibasin]
                dlonmax = lon_tmp[i]-basin_lon_max[ibasin]
                dlatmin = lat_tmp[i]-basin_lat_min[ibasin]
                dlatmax = lat_tmp[i]-basin_lat_max[ibasin]
                #print(dlonmin, dlonmax, dlatmin, dlatmax)
                if dlonmin*dlonmax < 0 and dlatmin*dlatmax <0:
                    TC_genesis_MJO_phase_basin[iph, ibasin] = TC_genesis_MJO_phase_basin[iph, ibasin] + 1
                    #print(ibasin)
                    continue

    # Save TC genesis number for 8 phases for each basin
    output2 = file_dir_out+'TC_genesis_number_9phase_basin_ACE2'+filstr+'1yr.npz'
    np.savez(output2, TC_genesis_MJO_phase_basin=TC_genesis_MJO_phase_basin, phase=np.arange(1,10),basin_list=basin_list)
else:
    data = np.load(file_dir_out+'TC_genesis_number_9phase_basin_ACE2'+filstr+'1yr.npz')
    TC_genesis_MJO_phase_basin = data['TC_genesis_MJO_phase_basin']


###########

# Use only summer season data (NH: May-Oct, SH: Nov-April)
# Updated 2025.3.2

calc_TC_genesis_phase_basin_summer = 1

if calc_TC_genesis_phase_basin_summer == 1:
    nphase = 9
    TC_genesis_MJO_phase_basin = np.zeros([nphase, nbasin])

    for iph in range(0, nphase):
        lon_tmp = globals()['lon_TC_phase'+str(iph+1)]
        lat_tmp = globals()['lat_TC_phase'+str(iph+1)]
        mon_tmp = globals()['mon_TC_phase'+str(iph+1)]
        for i in range(0, np.size(lon_tmp)):
            for ibasin in range(0, nbasin):
                dlonmin = lon_tmp[i]-basin_lon_min[ibasin]
                dlonmax = lon_tmp[i]-basin_lon_max[ibasin]
                dlatmin = lat_tmp[i]-basin_lat_min[ibasin]
                dlatmax = lat_tmp[i]-basin_lat_max[ibasin]
                #print(dlonmin, dlonmax, dlatmin, dlatmax)
                if dlonmin*dlonmax < 0 and dlatmin*dlatmax <0:
                    #if lat_tmp[i] > 0 and mon_tmp[i] <=10 and mon_tmp[i]>=5:
                    if lat_tmp[i] > 0 and mon_tmp[i] <=11 and mon_tmp[i]>=6:    # <--  this is where summer months are selected
                    #if lat_tmp[i] > 0 and mon_tmp[i] <=12 and mon_tmp[i]>=1:    # <--  this is where summer months are selected
                        TC_genesis_MJO_phase_basin[iph, ibasin] = TC_genesis_MJO_phase_basin[iph, ibasin] + 1
                        print(mon_tmp[i])
                        continue
                    elif lat_tmp[i] < 0 and (mon_tmp[i] >=11 or mon_tmp[i]<=4):
                        TC_genesis_MJO_phase_basin[iph, ibasin] = TC_genesis_MJO_phase_basin[iph, ibasin] + 1
                        #print(ibasin)
                        continue

    # Save TC genesis number for 8 phases for each basin
    # tc_genesis_file=file_dir2 + 'TC_genesis_1yr_'+yr+'_'+dstr+'_20'+ensnum+'.0_ace2.npz'
    output2 = file_dir_out+'TC_genesis_number_9phase_basin_ACE2'+filstr+'summer.npz'
    #output2 = file_dir_out+'TC_genesis_number_9phase_basin_ACE2'+filstr+'allmonths.npz'
    np.savez(output2, TC_genesis_MJO_phase_basin=TC_genesis_MJO_phase_basin, phase=np.arange(1,10),basin_list=basin_list)
    output3 = file_dir_out+'TC_genesis_number_9phase_basin_Comp_ACE2'+filstr+'summer.npz'
    #output3 = file_dir_out+'TC_genesis_number_9phase_basin_Comp_ACE2'+filstr+'allmonths.npz'
    #np.savez(output3, TC_genesis_MJO_phase_basin=TC_genesis_MJO_phase_basin, phase=np.arange(1,9),basin_list=basin_list)
    #output2 = file_dir_out+'MJO_8ph_composite_ACE2'+filstr+'1yr.npz'
    np.savez(output3, u850_8ph = u850_8ph, u200_8ph = u200_8ph, pr_8ph = pr_8ph, \
                    RMM_ind = RMM_ind,
                    pr_8ph_rms = pr_8ph_rms, u850_8ph_rms = u850_8ph_rms, u200_8ph_rms = u200_8ph_rms, \
                    TC_genesis_MJO_phase_basin=TC_genesis_MJO_phase_basin, phase=np.arange(1,10),basin_list=basin_list, \
                    time = time, lon = lon, lat = lat)

else:
    data = np.load(file_dir_out+'TC_genesis_number_9phase_basin_ACE2_2001_2010_summer_only.npz')
    TC_genesis_MJO_phase_basin = data['TC_genesis_MJO_phase_basin']



# Plot TC genesis for each MJO phase for each basin

# Calculate anomalous TC genesis for each basin
TC_genesis_MJO_phase_basin_ano = TC_genesis_MJO_phase_basin - np.mean(TC_genesis_MJO_phase_basin, 0)

print('size and shape of TC_genesis_MJO_phase_basin are: ',np.shape(TC_genesis_MJO_phase_basin),'size: ',np.size(TC_genesis_MJO_phase_basin))
print("the null set says, {user_input}...")
print("saved data files are here: ",file_dir_out)
print('output figures here: ',fig_dir_ace2)

print('the percentage of time that the MJO is in phases 1,2,3, or 8 during the Atlantic TC season is: ', valuep)

# LGS:  note that it is the TC genesis anomalies that are being plotted, just from the summer months....  
# try also looking at not just May-Oct but June-November and save the data for each of the different years.  
