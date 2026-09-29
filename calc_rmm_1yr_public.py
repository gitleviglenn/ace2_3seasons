####################################################################################################
# calc_rmm_1yr.py --> basically extracted from plot_rmm_1yr.py
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
# then run this, choosing the desired year
# $ python calc_rmm_1yr.py 2024
#
# The user needs to choose which phases of the MJO will be accounted for (mask_phase) and 
# which periods of time will be checked (mask_period)
#
# mask_phase
# mask_period
#
#
####################################################################################################
####################################################################################################
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
    yrstr = user_input

dirstr    = '/home/lsilvers/'

if ploc == "luft": # paths for luft
  dirstr2   = '/Users/C823281551/'
  fig_dir_ace2 = dirstr2 + 'figures/ace2_fig/MJO/'
  file_dir3 = dirstr2 + 'data/ACE2/'
  file_dir_out = file_dir3
  file_dir2 = file_dir3
  sys.path.append('/Users/C823281551/code/pythonCode/TC_genesis_ACE2_evaluation_public/function/')
else: # default paths are for maui
  dirstr2   = '/bell-scratch/C823281551/'
  file_dir3 = dirstr + 'data/ACE2/'
  file_dir_out = file_dir3
  file_dir2 = dirstr2 + 'ACE2/testout/'
  fig_dir_ace2 = dirstr2 + 'figure/ace2_fig/MJO/'
  sys.path.append('/home/C823281551/code/pythonCode/TC_genesis_ACE2_evaluation_public/function/')

import mjo_mean_state_diagnostics_uw as MJO

print('output directory is: ',file_dir_out)
#output = file_dir_out+'test_percentage_mjophase.npz'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bigFun(dstr, ensnum, yr):
    """
    Function to calculate the percentage of time the MJO is in a favorable phase for Atlantic TC activity for a given ensemble.
    """
    #filstr    = '_'+yr+'_'+dstr+'_'+ensnum+'_'

    #return filstr

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def compPercentage_rmm_timeseries(time, rmm1_norm, rmm2_norm, fig_dir_ace2, filstr, maskP):
        """
        Function to plot the RMM time series, excluding first and last times, and shading regions based on 8 MJO phases with pastel colors.
        """
        golden_ratio = (1 + 5**0.5) / 2
        fig = plt.figure(figsize=(12, 12 / golden_ratio))
        plt.rcParams.update({'font.size': 18})
        plt.ylabel('RMM1 and RMM2')
        #plt.title('time series')
    
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
        phase = np.full_like(rmm1_norm, np.nan)
        for it in range(len(rmm1_norm)):
            RMM1_tmp = rmm1_norm[it]
            RMM2_tmp = rmm2_norm[it]
            A = RMM1_tmp**2 + RMM2_tmp**2
            if A < 1:
                continue
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
        # it would probably be best to print which period is being used, and to control this
        # with a input parameter.
        if maskP < 1:
            mask_period = (time.dt.days > 151) & (time.dt.days <= 334)   # --> June through November
            print('CAUTION, masking period is from June through November!!') 
            timStr = 'June through November'
        elif maskP > 1:
            mask_period = (time.dt.days > 211) & (time.dt.days <= 273)  # --> August through September
            print('CAUTION, masking period is from August through September!!') 
            timStr = 'August through September'

        # do for each phase
        perc_arr_tmp = np.zeros(8)
        for tw in range(1, 9):
            mask_phase = np.isin(phase, tw)
            mask_rmm = (np.abs(rmm1_norm) > 1) | (np.abs(rmm2_norm) > 1)
            combined_mask = mask_phase & mask_rmm & mask_period
            perc_arr_tmp[tw-1] = np.sum(combined_mask) / np.sum(mask_period) * 100
        # end do 
        #mask_phase = np.isin(phase, [1, 2, 3, 8])
        mask_phase = np.isin(phase, [1, 2, 3])
        mask_rmm = (np.abs(rmm1_norm) > 1) | (np.abs(rmm2_norm) > 1)
        combined_mask = mask_phase & mask_rmm & mask_period
        percentage = np.sum(combined_mask) / np.sum(mask_period) * 100
        print(f"Percentage of time in phases 1,2,3 with |RMM| > 1 between {timStr}: {percentage:.2f}%")
        #print(f"Percentage of time in phases 1,2,3,8 with |RMM| > 1 between {timStr}: {percentage:.2f}%")
        
        return percentage, perc_arr_tmp
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #itit      = int(iti)
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
    #print("original p data: ")
    #print(ds)
    ds2       = xr.open_dataset(file_dir + file2, decode_timedelta=True)
    ds3       = xr.open_dataset(file_dir + file3, decode_timedelta=True)
    #
    
    #print("time is: ",ds.time.data)
    #print("attributes of ds are: ",ds.attrs) # it looks like the attributes of ds are an empty set
    #print("attributes of ds2 are: ",ds2.attrs) # it looks like the attributes of ds are an empty set
    print('~~~~~~~~~~~~~~~~~~~New~Wave~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('incoming precipitation file is: ',file_dir + file1)
    print('incoming wind file is: ',file_dir + file2)
    print('file dir out is: ',file_dir_out)
    print('~~~~~~~~~~~~~~~~~~~New~Wave~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
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
    #print('shape of time array is: ',np.shape(time))
    
    nt       = np.size(time)
    nlat     = np.size(lat_15SN)
    nlon     = np.size(lon)
    nmem     = np.size(mem)
    dt       = 4 # how many data points per day
    nday     = int(endtime/dt)
    nt       = endtime
    
    #print('number of lats is: ',np.size(lat))
    #print('number of times is: ',np.size(time))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # first read and select data on/at the appropriate times/levels.
    
    lat_15S = ds.lat.sel(lat=-15, method="nearest")
    lat_15N = ds.lat.sel(lat=15, method="nearest")
    
    u850a  = ds2['eastward_wind'][0:endtime,:,:]
    u200a  = ds3['eastward_wind'][0:endtime,:,:]
    PRECIP = ds['PRATEsfc'][0,0:endtime,:,:]
    V      = PRECIP.transpose("time","lat","lon").values
    u850   = u850a.transpose("time","lat","lon").values
    u200   = u200a.transpose("time","lat","lon").values
    
    #print('shape of V is: ',np.shape(V))
    #print('shape of u850 is: ',np.shape(u850))
    #print('shape of u200 is: ',np.shape(u200))
    
    V_reshape    = np.reshape(V, (nday, dt, nlat, nlon))
    u850_reshape = np.reshape(u850, (nday, dt, nlat, nlon))
    u200_reshape = np.reshape(u200, (nday, dt, nlat, nlon))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # calculate diurnal cycle to remove it
    
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
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # calculate meridional average
    # Calculate the meridional average of the precipitation
    lat_radians = np.deg2rad(lat) 
    weights     = np.cos(lat_radians)
    pr_15SN_ano = (pr_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(pr_ano)).sum(dim="lat", skipna=True)
    u850_15SN_ano = (u850_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(u850_ano)).sum(dim="lat", skipna=True)
    u200_15SN_ano = (u200_ano * weights).sum(dim="lat", skipna=True) / weights.where(~np.isnan(u200_ano)).sum(dim="lat", skipna=True)
    #print("shape of pr_15SN_ano is: ",np.shape(pr_15SN_ano))   
    #print("shape of u850_15SN_ano is: ",np.shape(u850_15SN_ano))
    #print("shape of u200_15SN_ano is: ",np.shape(u200_15SN_ano))
    
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
    
    ## find nans
    #print(np.sum(np.isnan(pr_final)))
    #print(np.sum(np.isnan(u850_final)))
    #print(np.sum(np.isnan(u200_final)))
    #
    #print(np.shape(pr_final))
    #print(np.shape(u850_final))
    #print(np.shape(u200_final))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Use EOF from ERA5 to construct the RMM index in ACE2
    
    X, mu_u850, std_u850, mu_u200, std_u200, mu_pr, std_pr = MJO.normalize_before_ceof(u850_final,u200_final, pr_final)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Use pr, u200, u850 to construct RMM index. 
    # EOF Analysis
    data = np.load(file_dir3 + 'MJO_EOF_ERA5_2001_2010.npz')
    EOF  = data['EOF']
    #print('ERA5 EOF file is: ',file_dir3+'MJO_EOF_ERA5_2001_2010.npz')
    
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
    
    rmm1 = PC[0] #or -PC[0]. you may want to check this by doing the phase composite (this could also be negative) (Check if each phase corresponds to the correct enhanced convection region)!
    rmm2 = PC[1] #or -PC[1]. you may want to check this by doing the phase composite (this could also be negative)!
    
    #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #print('shape and size of rmm1 and rmm2 are: ',np.shape(rmm1),' and ',np.size(rmm1))
    #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    '''
    RMM 8 phase index
    '''
    time_val = time.values
    n,RMM_ind,rmm1_norm,rmm2_norm = MJO.rmm_eight_phase_index(rmm1,rmm2,time,rmm1,rmm2)
    
    
    # this is the call to the function that computes the percentage of time the MJO is in a favorable phase for 
    # atlantic TCs.
    mp = 2. # defines the masking period.  mp = 0. should be june through november.  mp = 2 should be august and september
    valuep,values = compPercentage_rmm_timeseries(time, rmm1_norm, rmm2_norm, fig_dir_ace2, filstr, mp)
    
    print('the percentage of time that the MJO is in phases 1,2,3, or 8 during the Atlantic TC season is: ', valuep)

    return valuep, values

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

comp_mjo_heatmap = 'no'

# run the bigFun function over all ensemble members:
if comp_mjo_heatmap == 'yes':
    ensarr    = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    decarr    = ['dec01', 'dec02', 'dec03', 'dec04']
    
    perc_arr = np.zeros(40)
    perc_arr_ph = np.zeros((40,8))
    
    totind=0
    #for ind in range(0, 2):
    for ind in range(0, 10):
        green = ensarr[ind]
        for ind2 in range(0, 4):
        #for ind2 in range(0, 1):
            blue = decarr[ind2]
            #red = '2024'
            red = yrstr
            pythong,pythongs = bigFun(blue, green, red)
            print('output from bigFun is: ',pythong)
            perc_arr[totind] = pythong
            perc_arr_ph[totind,:] = pythongs
            totind = totind + 1
    
    output = file_dir_out+'Grid_percentage_mjophase_'+yrstr+'_augsep.npz'
    np.savez(output, perc_arr=perc_arr,perc_arr_mjo_phase=perc_arr_ph)

#print('output file should be here: ',file_dir_out+'test_percentage_mjophase.npz')
#print('percentage array for ',red,' is: ',perc_arr[:])
#print('mean percentage array for ',red,' is: ',np.mean(perc_arr,axis=0))
#
####def bigFun(dstr, ensnum, yr):

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# process the individual ensembles desired: 

yr2plot = yrstr
# these are for the active years: 
if yr2plot == '2024':
    yr        = '2024'
    #hinum = 5 # number of high end ensembles
    ## 13, 0, 12, 34, 1
    #ensarr    = ['04', '01', '03', '05', '02']
    #decarr    = ['dec02', 'dec01', 'dec02', 'dec04', 'dec01']
    #
    hinum = 9
    ensarr    = ['01',    '02',    '09',    '03',    '04',    '10',    '02',    '05',    '06']
    decarr    = ['dec01', 'dec01', 'dec01', 'dec02', 'dec02', 'dec03', 'dec04', 'dec04', 'dec04']
    # 0, 1, 8, 12, 13, 29, 31, 34, 35 --> additional ensembles (everything above 3rd quartile)
    # 1, 2, 9, 13, 14, 30, 32, 35, 36
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    #hinum = 5 # number of high end ensembles
    ## 8, 21, 17, 27, 28 
    #ensarr    = ['09', '02', '08', '08', '09']
    #decarr    = ['dec01', 'dec03', 'dec02', 'dec03', 'dec03']
    #
    hinum = 9 # number of high end ensembles
    ensarr    = ['09'   , '01'   , '08'   , '01'   , '02'   , '08'   , '09'   , '04'   , '08']
    decarr    = ['dec01', 'dec02', 'dec02', 'dec03', 'dec03', 'dec03', 'dec03', 'dec04', 'dec04']
    # 8, 10, 17, 20, 21, 27, 28, 33, 37
    # 9, 11, 18, 21, 22, 28, 29, 34, 38
else:
    yr        = '2005'
    # 16, 1, 9, 2, 11
    #hinum = 5 # number of high end ensembles
    #ensarr    = ['06', '01', '09', '02', '01']
    #decarr    = ['dec02', 'dec01', 'dec01', 'dec01', 'dec02']
    hinum = 7 # number of high end ensembles
    ensarr    = ['01'   , '02'   , '09'   , '01'   , '06'   , '05'   , '05']
    decarr    = ['dec01', 'dec01', 'dec01', 'dec02', 'dec02', 'dec03', 'dec04']
    # 0, 1, 8, 10, 15, 24, 34 --> additional ensembles (everything above the 3rd quartile)
    # 1, 2, 9, 11, 16, 25, 35



hi_perc_arr = np.zeros(hinum)
hi_perc_arr_ph = np.zeros((hinum,8))

totind=0
for ind in range(0, hinum):
    green = ensarr[ind]
#    for ind2 in range(0, hinum):
    blue = decarr[ind]
#        #red = '2024'
    red = yrstr
    pythong,pythongs = bigFun(blue, green, red)
    print('output from bigFun is: ',pythong)
    hi_perc_arr[totind] = pythong
    hi_perc_arr_ph[totind,:] = pythongs
    totind = totind + 1
#
print("~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~")



# these are for the inactive years: 
if yr2plot == '2024':
    yr        = '2024'
    #lonum = 5 # number of low end ensembles
    ## 33, 37, 5, 39, 7 --> shifted by +1 to match ensemble naming
    #ensarr_lo    = ['03', '07', '05', '09', '07']
    #decarr_lo    = ['dec04', 'dec04', 'dec01', 'dec04', 'dec01']
    lonum = 8 # number of low end ensembles
    ensarr_lo    = ['03', '04', '07', '02', '01', '03', '07', '09']
    decarr_lo    = ['dec01', 'dec01', 'dec01', 'dec03', 'dec04', 'dec04', 'dec04', 'dec04']
    # 2, 4, 6, 21, 30, 32, 36, 38 --> additional ensembles (everything below 1st quartile)
    # 3, 4, 7, 22, 31, 33, 37, 39 --> shift by 1 to match the labelling of individual ensembles
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    #lonum = 5 # number of low end ensembles
    ## 20, 26, 32, 35, 15
    #ensarr_lo    = ['10', '06', '02', '05', '05']
    #decarr_lo    = ['dec02', 'dec03', 'dec04', 'dec04', 'dec02']
    lonum = 10 # number of low end ensembles
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


print("~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~")


lo_perc_arr = np.zeros(lonum)
lo_perc_arr_ph = np.zeros((lonum,8))

totind=0
for ind in range(0, lonum):
    green = ensarr_lo[ind]
    blue = decarr_lo[ind]
    red = yrstr
    pythong,pythongs = bigFun(blue, green, red)
    print('output from bigFun is: ',pythong)
    lo_perc_arr[totind] = pythong
    lo_perc_arr_ph[totind,:] = pythongs
    totind = totind + 1
#

print("~~~~~~~~~~~~~~~~~~~~")
print('percentage array for quiet ',red,' is: ',lo_perc_arr[:])
print('mean percentage array for quiet ',red,' is: ',np.mean(lo_perc_arr,axis=0))

print("~~~~~~~~~~~~~~~~~~~~")
print('percentage array for active ',red,' is: ',hi_perc_arr[:])
print('mean percentage array for active ',red,' is: ',np.mean(hi_perc_arr,axis=0))


#pythong,pythongs = bigFun('dec02', '04', yrstr)
#print('output from bigFun is: ',pythong)

if comp_mjo_heatmap == 'yes':
    print("~~~~~~~~~~~~~~~~~~~~")
    print('output file should be here: ',file_dir_out+'test_percentage_mjophase.npz')
    print('percentage array for ',red,' is: ',perc_arr[:])
    print('mean percentage array for ',red,' is: ',np.mean(perc_arr,axis=0))


#print('individual values: ',perc_arr[0],' ',perc_arr[1],' ',perc_arr[12],' ',perc_arr[13],' ',perc_arr[34])
#print("~~~~~~~~~~~~~~~~~~~~")
#print('individual values: ',perc_arr[0],' ',perc_arr[5],' ',perc_arr[10],' ',perc_arr[14],' ',perc_arr[20])





