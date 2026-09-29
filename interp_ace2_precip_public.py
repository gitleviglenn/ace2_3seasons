##################################################################################################
# interpolate wind and precip data to a 2.5 degree grid between 15S and 15N and then write out   #
# the results to netcdf files.                                                #
#
# in which script are the autoregressive_prediction files created? 
# here: ace2_pp_driver_public.sh
#
# the present script has the following input and output:
# input:  autoregressive_predictions_2013_dec01_02_PRATEsfc_b.nc 
# output: int_prec_2013_dec01_02_b.nc
#
# after the output is created from this script it needs to be copied to the desired directory
#
# levi silvers                                                                          feb 2026 #
##################################################################################################

import numpy as np
import xarray as xr
import os

dirstr  = '/data/ACE2/'
#fig_dir  = dirstr2 + 'figure/ace2_fig/' # Remote direcotry for figures 
#os.makedirs(fig_dir,exist_ok=True) 
#file_name = 'autoregressive_predictions_1yr.nc'
#file_name = 'autoregressive_predictions.nc'  # this should have 10 years of data...


print("dirstr is: ",dirstr)
#file_name = "autoregressive_predictions_2024_dec03_10_PRATEsfc.nc"
file_dir = dirstr 

#ds      = xr.open_dataset(file_dir + file_name) #(time, ensemble_member, lat, lon)          # precip data
#PRECIP  = ds['PRATEsfc'][:,:,74:106,:]
#lat_15S = ds.lat.sel(lat=-15, method="nearest")
#lat_15N = ds.lat.sel(lat=15, method="nearest")

lat_2p5deg = np.arange(-15, 17.5, 2.5)
lon_2p5deg = np.arange(0, 360, 2.5)

#int_prec    = PRECIP.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')

yrs = list(['2013', '2005', '2024'])
dcs = list(['dec02','dec01','dec03','dec04'])
ens = list(['01','02','03','04','05','06','07','08','09','10'])
blah = 1
for y in range(0,3):
    print(yrs[y])
    for d in range(1,4):
        print(dcs[d])
        for e in range(0,10):
            file_name="autoregressive_predictions_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_PRATEsfc_b.nc"
            ds      = xr.open_dataset(file_dir + file_name) #(time, ensemble_member, lat, lon)          # precip data
            PRECIP  = ds['PRATEsfc'][:,:,74:106,:]
            lat_15S = ds.lat.sel(lat=-15, method="nearest")
            lat_15N = ds.lat.sel(lat=15, method="nearest")
            int_prec    = PRECIP.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')
            op_f1 = "int_prec_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_b.nc"
            int_prec.to_netcdf(op_f1)
            blah = blah + 1
            print("op_f1")
            print("autoregressive_predictions_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_PRATEsfc.nc")
            print("blah is: "+str(blah))

print("dirstr is: ",dirstr)
print("scumstash")
