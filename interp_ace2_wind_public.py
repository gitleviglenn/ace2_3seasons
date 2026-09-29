##################################################################################################
# interpolate ERA5 data to 2.5 degree grid for use in MJO diagnostics
#
# interpolate wind data to a 2.5 degree grid between a chosen lat rangeand then write out 
# the results to an npz file and to netcdf files in the working directory.  
#
# it looks to me like there is not much metadata saved to the npz files.   is that true? 
#
# this script needs to be run for each 5 year chunk of ensembles of each year.   
# so we need to run it 8 times per year.
#
# for reference see E1.1_Find_rmm_ace2_2001_2010.ipynb
# 
# levi silvers                                                                           oct 2025
##################################################################################################

import numpy as np
import xarray as xr
import sys
import os

#DIR  = '/Users/C823281551/data/ACE2/'
dirstr1  = '/bell-scratch/C837469599/'
dirstr2  = '/bell-scratch/C823281551/'
#DIR2 = '/Users/C823281551/data/ERA5/'
fig_dir  = dirstr2 + 'figure/ace2_fig/' # Remote direcotry for figures 
os.makedirs(fig_dir,exist_ok=True) 
#file_name = 'autoregressive_predictions_1yr.nc'
file_name = 'autoregressive_predictions.nc'  # this should have 10 years of data...

if len(sys.argv) > 0:
    user_input = sys.argv[1]
    yr_str = user_input
    print(f"scumstash says input decade string is, {user_input}...")
    user_input = sys.argv[2]
    yr = user_input
    print(f"scumstash says input year string is, {user_input}...")

# these should be set using user_input, see above
#yr_str   = '2'
#yr       = '2005'

# choose which 5 year chunk to process
#yrrange  = '6-10'
yrrange  = '1-5'

d_str    = 'dec0'+yr_str
#file_dir = dirstr1 + 'data_output/ace2/ace2_output/yr'+yr_str+'/'
file_dir = dirstr1 + 'ACE2_share/ACE2_simulation_output/'+yr+'/dec0'+yr_str+'/'
# the u-dile has 5 years of data.

# this works for most files, but there are a few that are out of place.  
#file_u1   = dirstr1 + 'ACE2_share/ACE2_simulation_output/'+yr+'/dec0'+yr_str+'/pressure_coordinate/' + 'P-coord_ace2_u_'+yr+'_yr'+yrrange+'.nc'  # wind data

# this alternate path is needed for the 3rd decade of 2005 data for the years 1-5.
file_u1   = dirstr1 + 'ACE2_share/ACE2_simulation_output/'+yr+'/dec0'+yr_str+'/' + 'P-coord_ace2_u_'+yr+'_yr'+yrrange+'.nc'  # wind data

#file_u1   = dirstr1 + 'ACE2_share/ACE2_simulation_output/'+yr+'/dec0'+yr_str+'/pressure_coordinate/' + 'P-coord_ace2_u_'+yr+'_yr6-10.nc'  # wind data

ds      = xr.open_dataset(file_dir + file_name) #(time, ensemble_member, lat, lon)          # precip data
#PRECIP  = ds['PRATEsfc'][:,:,74:106,:]
#lat_15S = ds.lat.sel(lat=-15, method="nearest")
#lat_15N = ds.lat.sel(lat=15, method="nearest")
lat_15S = ds.lat.sel(lat=-30, method="nearest")
lat_15N = ds.lat.sel(lat=30, method="nearest")

ds2     = xr.open_dataset(file_u1)
#ds2a     = xr.open_dataset(file_u1)
#ds2b    = xr.open_dataset(file_u2)

# merge the two 5 years chunks of eastward_wind data:
#ds2 = ds2a.merge(ds2b)

plev   = ds2['plev'] 
lat    = ds2['lat'] # --> this results in an xarray.DataArray object 'lat'

#time1  = ds2a['time']
#time2  = ds2b['time']

#print('lats are: ',lat)
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('file1 is: ',file_u1)
#print('times 1 are: ',time1[0:40])
#print('last times 1 are: ',time1[-20:])
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('file1 is: ',file_u2)
#print('times 2 are: ',time2[0:40])
#print('last times 2 are: ',time2[-20:])
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

ds2a       = ds2.sel(plev=200, drop=True)
ds2b       = ds2.sel(plev=slice(800, 900), drop=True)
u850_temp  = ds2b['eastward_wind'].mean(dim="plev")
u850       = u850_temp.sel(lat=slice(lat_15S, lat_15N))
u200_temp  = ds2a['eastward_wind']
u200       = u200_temp.sel(lat=slice(lat_15S, lat_15N))

#lat        = u850['lat']
#print('lats are: ',lat)

print('what is u850? ',np.size(u850))
print('what is u850? ',np.shape(u850))
print('what is u200? ',np.shape(u200))

####
# Set the domain to interpolate onto: Interpolate the data into 2.5 deg
#lat_2p5deg = np.arange(-15, 17.5, 2.5)
#dom_str = 'pm15'

lon_2p5deg = np.arange(0, 360, 2.5)

lat_2p5deg = np.arange(-30, 32.5, 2.5)
dom_str = 'pm30'
####

#int_prec    = PRECIP.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')
int_u850    = u850.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')
int_u200    = u200.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')

## now I need to write the results out to a file that can be opened up in a notebook.  
#np.savez('interp_wind_precip.npz', precip=int_prec, u850 = int_u850, u200 = int_u200)

#op_f1 = "int_prec_"+yr+d_str+"_yr6-10.nc"
#op_f2 = "int_u850_"+yr+d_str+"_yr6-10.nc"
#op_f3 = "int_u200_"+yr+d_str+"_yr6-10.nc"

op_f2 = "int_u850_"+yr+d_str+"_yr"+yrrange+"_"+dom_str+".nc"
op_f3 = "int_u200_"+yr+d_str+"_yr"+yrrange+"_"+dom_str+".nc"

#int_prec.to_netcdf(op_f1)
int_u850.to_netcdf(op_f2)
int_u200.to_netcdf(op_f3)
print(f"wind data saved to {op_f2}, and {op_f3}")



