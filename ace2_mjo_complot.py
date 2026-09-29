#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ace2_complot.py
#
# this scripts creates several plots.   two plots show the TC count # as a function of MJO 
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

#yr        = '2024'
#dstr      = 'dec01'
#ensnum    = '01'
#filstr    = '_'+yr+'_'+dstr+'_'+ensnum+'_'

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
    # 13, 0, 12, 34, 1
    ensarr    = ['04', '01', '03', '05', '02']
    decarr    = ['dec02', 'dec01', 'dec02', 'dec04', 'dec01']
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    # 8, 21, 17, 27, 28 
    ensarr    = ['09', '02', '08', '08', '09']
    decarr    = ['dec01', 'dec03', 'dec02', 'dec03', 'dec03']
else:
    yr        = '2005'
    # 13, 0, 12, 34, 1
    ensarr    = ['06', '01', '09', '02', '01']
    decarr    = ['dec02', 'dec01', 'dec01', 'dec01', 'dec02']

# these are for the inactive years: 
if yr2plot == '2024':
    yr        = '2024'
    # 33, 37, 5, 39, 7
    ensarr_lo    = ['03', '07', '05', '09', '07']
    decarr_lo    = ['dec04', 'dec04', 'dec01', 'dec04', 'dec01']
elif yr2plot == '2013':
    #print('pick a year nimrod')
    yr        = '2013'
    # 20, 26, 32, 35, 15
    ensarr_lo    = ['10', '06', '02', '05', '05']
    decarr_lo    = ['dec02', 'dec03', 'dec04', 'dec04', 'dec02']
else:
    yr        = '2005'
    # 23, 32, 20, 24, 40 
    ensarr_lo    = ['03', '02', '10', '04', '10']
    decarr_lo    = ['dec03', 'dec04', 'dec02', 'dec03', 'dec04']

#index = 8
#print('size and shape of u850_8ph are: ',np.size(u850_8ph),' and ',np.shape(u850_8ph))
hi_stars = np.zeros((5,8))
lo_stars = np.zeros((5,8))
all_stars = np.zeros((40,8))

const_u850 = np.zeros((5,8,13,144))
const_u200 = np.zeros((5,8,13,144))
const_pr   = np.zeros((5,8,13,144))
# for the low activity years:
const_u850_lo = np.zeros((5,8,13,144))
const_u200_lo = np.zeros((5,8,13,144))
const_pr_lo   = np.zeros((5,8,13,144))
#size and shape of u850_8ph are:  14976  and  (8, 13, 144)

# combine individual ensemble members into 1 array for processing.  
for ind in range(0, 5):
    ensnum  = ensarr[ind]
    dstr    = decarr[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
    f1a     = np.load(file_dir2+file)
    TC_f1a  = f1a['TC_genesis_MJO_phase_basin']
    hi_stars[ind,:] = TC_f1a[:,3]
    print(f1a.files)
    print('file string',filstr)
    print('file ',file)
    print('index is',ensarr[ind])
    file2   = 'MJO_8ph_composite_ACE2'+filstr+'1yr.npz'
    f2a     = np.load(file_dir2+file2)
    temp1 = f2a['u850_8ph']
    temp2 = f2a['u200_8ph']
    temp3 = f2a['pr_8ph']
    const_u850[ind,:,:,:] = temp1[:,:,:]
    const_u200[ind,:,:,:] = temp2[:,:,:]
    const_pr[ind,:,:,:] = temp3[:,:,:]
    print('high file2 is',file2)
    print(f2a.files)

# combine individual ensemble members into 1 array for processing.  
for ind in range(0, 5):
    ensnum  = ensarr_lo[ind]
    dstr    = decarr_lo[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
    #f1a     = np.load(file_dir2+file)
    #TC_f1a  = f1a['TC_genesis_MJO_phase_basin']
    #hi_stars[ind,:] = TC_f1a[:,3]
    #print(f1a.files)
    #print('file string',filstr)
    #print('file ',file)
    print('index is',ensarr_lo[ind])
    file2   = 'MJO_8ph_composite_ACE2'+filstr+'1yr.npz'
    f2a     = np.load(file_dir2+file2)
    temp1 = f2a['u850_8ph']
    temp2 = f2a['u200_8ph']
    temp3 = f2a['pr_8ph']
    const_u850_lo[ind,:,:,:] = temp1[:,:,:]
    const_u200_lo[ind,:,:,:] = temp2[:,:,:]
    const_pr_lo[ind,:,:,:] = temp3[:,:,:]
    print('low file2 is',file2)
    print(f2a.files)

#int_2005_dec02_05_u200_b.nc
endtime = 1460 # 1 year
filenc   = file_dir2+'int'+filstr+'u200_b.nc'
ds       = xr.open_dataset(filenc)
lat_15SN = ds['lat'][:]
lat      = ds['lat']
lon      = ds['lon']
temptime = ds['time']
time     = temptime[0:endtime]

mn_hi_stars = np.mean(hi_stars,axis=0) # compute the mean value along each MJO phase
mn_hi_stars

comp_mn_u850 = np.mean(const_u850,axis=0) # average over the ensemble members
comp_mn_u200 = np.mean(const_u200,axis=0) # average over the ensemble members
comp_mn_pr   = np.mean(const_pr,axis=0) # average over the ensemble members

comp_mn_lo_u850 = np.mean(const_u850_lo,axis=0) # average over the ensemble members
comp_mn_lo_u200 = np.mean(const_u200_lo,axis=0) # average over the ensemble members
comp_mn_lo_pr   = np.mean(const_pr_lo,axis=0) # average over the ensemble members


#if yr2plot == '2024':
#    yr        = '2024'
#    # 32, 36, 4, 38, 6
#    ensarr    = ['03', '07', '05', '09', '07']
#    decarr    = ['dec04', 'dec04', 'dec01', 'dec04', 'dec01']
#elif yr2plot == '2013':
#    yr        = '2013'
#    ensarr    = ['10', '06', '02', '05', '05']
#    decarr    = ['dec01', 'dec02', 'dec03', 'dec03', 'dec02']
#else:
#    yr        = '2005'
#    ensarr    = ['03', '02', '10', '04', '10']
#    decarr    = ['dec03', 'dec04', 'dec02', 'dec03', 'dec04']

#index = 8
for ind in range(0, 5):
    ensnum  = ensarr[ind]
    dstr    = decarr[ind]
    filstr  = '_'+yr+'_'+dstr+'_'+ensnum+'_'
    file    = 'TC_genesis_number_8phase_basin_ACE2'+filstr+'summer.npz'
    fa      = np.load(file_dir2+file)
    TC_fa   = fa['TC_genesis_MJO_phase_basin']
    lo_stars[ind,:] = TC_fa[:,3]
    print(fa.files)
    print('file string',filstr)
    print('index is',ensarr[ind])

mn_lo_stars = np.mean(lo_stars,axis=0) # compute the mean value along each MJO phase
mn_lo_stars


# go big or go home 
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

nphase = 8
ibasin = 3
#for ibasin in range(0, nbasin):
zeros = np.zeros([nphase])
phase = np.arange(1,9)
    #plt.plot(phase, TC_genesis_MJO_phase_basin_ano[:,ibasin]/10)
fig, ax = plt.subplots()
plt.plot(phase, hi_stars[0,:]/1, label='one')
plt.plot(phase, hi_stars[1,:]/1, label='two')
plt.plot(phase, hi_stars[2,:]/1, label='three')
plt.plot(phase, hi_stars[3,:]/1, label='four')
plt.plot(phase, hi_stars[4,:]/1, label='five')
plt.plot(phase, mn_hi_stars[:], 'k--', label='mean') # mean values for each MJO phase
plt.legend(loc="upper right")
#plt.plot(phase, zeros, 'k--')
plt.title(basin_list[ibasin]+', ACE2 (5 active ensemble members from the '+yr+' season)')
plt.xticks(phase)
plt.ylim(-0.5, 5.5)
plt.xlabel('MJO phase')
plt.ylabel('TC genesis (#/yr)')
plt.show()
# mn_hi_stars = np.mean(hi_stars,axis=0)

fig.savefig('top5_'+yr2plot+'.png', dpi=300)

nphase = 8
ibasin = 3
#for ibasin in range(0, nbasin):
zeros = np.zeros([nphase])
phase = np.arange(1,9)
    #plt.plot(phase, TC_genesis_MJO_phase_basin_ano[:,ibasin]/10)
fig, ax = plt.subplots()
plt.plot(phase, lo_stars[0,:]/1, label='one')
plt.plot(phase, lo_stars[1,:]/1, label='two')
plt.plot(phase, lo_stars[2,:]/1, label='three')
plt.plot(phase, lo_stars[3,:]/1, label='four')
plt.plot(phase, lo_stars[4,:]/1, label='five')
plt.plot(phase, mn_lo_stars[:], 'k--', label='mean') # mean values for each MJO phase
plt.legend(loc="upper right")
#plt.plot(phase, zeros, 'k--')
plt.title(basin_list[ibasin]+', ACE2 (5 quite ensemble members from the '+yr+' season)')
plt.xticks(phase)
plt.ylim(-0.5, 5.5)
plt.xlabel('MJO phase')
plt.ylabel('TC genesis (#/yr)')
plt.show()
# mn_hi_stars = np.mean(hi_stars,axis=0)

fig.savefig('bottom5_'+yr2plot+'.png', dpi=300)

nphase = 8
ibasin = 3
#for ibasin in range(0, nbasin):
zeros = np.zeros([nphase])
phase = np.arange(1,9)
    #plt.plot(phase, TC_genesis_MJO_phase_basin_ano[:,ibasin]/10)
fig, ax = plt.subplots()
for ii in range(0, 40):
    plt.plot(phase, all_stars[ii,:]/1, label='one')
plt.plot(phase, mn_all_stars[:], 'k--', label='mean') # mean values for each MJO phase
#plt.legend(loc="upper right")
plt.title(basin_list[ibasin]+', ACE2 (all ensemble members from the '+yr+' season)')
plt.xticks(phase)
plt.ylim(-0.5, 5.5)
plt.xlabel('MJO phase')
plt.ylabel('TC genesis (#/yr)')
plt.show()

fig.savefig('all40_'+yr2plot+'.png', dpi=300)

# work on plotting fields of the composite variables:
'''
Plot rmm 8-phases composite: olr, u850, u200
'''


###data     = np.load(file_dir_out+'MJO_8ph_composite_ACE2_2001_2010.npz')1
##RMM_ind  = f2a['RMM_ind']
#u850_8ph = f2a['u850_8ph']
#u200_8ph = f2a['u200_8ph']
#pr_8ph   = f2a['pr_8ph']
#u850_8ph = comp_mn_u850
u200_8ph = comp_mn_u200
vws_8ph  = comp_mn_u200 - comp_mn_u850
u850_8ph = comp_mn_u850
pr_8ph   = comp_mn_pr

u200_lo_8ph = comp_mn_lo_u200
vws_lo_8ph  = comp_mn_lo_u200 - comp_mn_lo_u850
u850_lo_8ph = comp_mn_lo_u850
pr_lo_8ph   = comp_mn_lo_pr

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
print('size and shape of u850_8ph are: ',np.size(u850_8ph),' and ',np.shape(u850_8ph))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')

# plot all three variables, both for high and low ensemble members
vname_long = list(['precipitation (mm/day)','u850 (m/s)','u200 (m/s)'])
vname = list(['pr','u850','u200'])

# plot the vws for high ensemble members, and for low ensemble members
vnamevws = list(['vws','vws_lo'])
vname_vws_long = list(['vws high numbers','vws low members'])

model_name = 'ERA5'
cmap_list = list(['RdBu','RdBu_r','RdBu_r'])

# Set Contour Level
clev1 = np.arange(-5,5.5,0.5) # pr
cticks1 = np.arange(-5,6,1)
clev2 = np.arange(-5,5.5,0.5) # u850
cticks2 = np.arange(-5,6,1)
clev3 = np.arange(-10, 11, 1) # u200
cticks3 = np.arange(-10, 12, 2)

# plot active ensemble members
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
    fig_name = 'Fig_8phase_5ensembleComp'+filstr+vname[v]+'.png'

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
    #plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    plt.close()

# plot inactive ensemble members
for v in range(0,3):#np.size(vname)):
    v_in = globals()[vname[v]+'_lo_8ph']
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
    fig_name = 'Fig_8phase_5ensemble_low_Comp'+filstr+vname[v]+'.png'

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
    #plt.savefig(fig_dir_ace2+fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    plt.close()

# plot inactive ensemble members
for v in range(0,2):#np.size(vname)):
    v_in = globals()[vnamevws[v]+'_8ph']
    #clev = globals()['clev'+str(v+1)]
    clev = clev3 # globals()['clev'+str(v+1)]
    cticks = globals()['cticks'+str(v+1)]
    if v == 0: #moisture/pr (blue positive, red negative)
        cbar = "RdBu_r"
    else:
        cbar = "RdBu_r"

    if v == 0:
        scalef = 1.
    else:
        scalef = 1.

    #fig_name = 'Fig.1_MJO_8phase_composite_'+yr+dstr+'_'+vname[v]+'.png'
    print('The value of vnammevws[v] is: ',vnamevws[v]+'_8ph')
    fig_name = 'Fig_8phase_5ensemble_Comp'+filstr+vnamevws[v]+'.png'

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

    plt.suptitle('MJO composite '+vname_vws_long[v]+' (ACE2, 1yr)', y=0.96)

    cb = fig.colorbar(contour, ax=axes[:], orientation='horizontal',shrink=0.6, fraction=0.05, pad=0.05, aspect=40)
    cb.ax.tick_params(labelsize=6)
    cb.set_ticks(cticks)
    plt.savefig(fig_name,format='png', dpi=600) # Change this to be fig_dir_ace2 if using ace data
    plt.close()



