##################################################################################################
# interpolate TWP data to a 2.5 degree grid between 30S and 30N and then write out               #
# the results to a netcdf files.                                                                 #
#
# in which script are the autoregressive_prediction files created? 
# here: ace2_pp_driver_public.sh
#
# the present script has the following input and output:
# input:  autoregressive_predictions_2013_dec01_02_TWP_b.nc 
# output: int_TWP_2013_dec01_02_b.nc
#
# after the output is created from this script it needs to be copied to the desired directory
#
# levi silvers                                                                          feb 2026 #
##################################################################################################

import numpy as np
import xarray as xr
import os

dirstr  = '/data/ACE2/'

print("dirstr is: ",dirstr)
file_dir = dirstr 

#lat_2p5deg = np.arange(-15, 17.5, 2.5)
lat_2p5deg = np.arange(-30, 32.5, 2.5)
lon_2p5deg = np.arange(0, 360, 2.5)

yrs = list(['2013', '2005', '2024'])
dcs = list(['dec02','dec01','dec03','dec04'])
ens = list(['01','02','03','04','05','06','07','08','09','10'])
blah = 1
for y in range(0,3):
    print(yrs[y])
    for d in range(0,4):
        print(dcs[d])
        for e in range(0,10):
            file_name="autoregressive_predictions_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_TWP_b.nc"
            ds      = xr.open_dataset(file_dir + file_name) #(time, ensemble_member, lat, lon)          # TWP data
            TWP     = ds['total_water_path'][:,:,59:121,:]
            lat_15S = ds.lat.sel(lat=-30, method="nearest")
            lat_15N = ds.lat.sel(lat=30, method="nearest")
            int_TWP    = TWP.interp(lat=lat_2p5deg,lon=lon_2p5deg, method='linear')
            op_f1 = "int_TWP_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_b.nc"
            int_TWP.to_netcdf(op_f1)
            blah = blah + 1
            print("op_f1")
            print("autoregressive_predictions_"+yrs[y]+"_"+dcs[d]+"_"+ens[e]+"_TWP.nc")
            print("blah is: "+str(blah))

#op_f1 = "int_prec_"+yr+d_str+"_yr6-10.nc"

#int_prec.to_netcdf(op_f1)
print("dirstr is: ",dirstr)
print("scumstash")
#print(f"precip data saved to {op_f2}, and {op_f3}")
