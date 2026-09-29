#--------------------------------------------------------------------------------------------
# produces a 3 panel figure showing the percentage of time in which each ensemble 
# member resides in favorable mjo phases. 
#
# this script just makes the figures after opening up the 3 npz data files: 
# 'Grid_percentage_mjophase05.npz'
# 'Grid_percentage_mjophase13.npz'
# 'Grid_percentage_mjophase24.npz'
# 
# which script creates those three data files?   --> perhaps the calc_rmm_1yr,py script?
# 
# levi silvers                                                                     july 2026
#--------------------------------------------------------------------------------------------


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dir='/home/lsilvers/data/ACE2/'

#file1='Grid_percentage_mjophase05.npz'
#file2='Grid_percentage_mjophase13.npz'
#file3='Grid_percentage_mjophase24.npz'
file1='Grid_percentage_mjophase05_augsep.npz'
file2='Grid_percentage_mjophase13_augsep.npz'
file3='Grid_percentage_mjophase24_augsep.npz'

with np.load(dir+file1) as data: 
    print(f"Arrays in the file:  {data.files}")
    array1 = data['perc_arr']
    array2 = data['perc_arr_mjo_phase'] 

with np.load(dir+file2) as data: 
    print(f"Arrays in the file:  {data.files}")
    array1b = data['perc_arr']
    array2b = data['perc_arr_mjo_phase'] 

with np.load(dir+file3) as data: 
    print(f"Arrays in the file:  {data.files}")
    array1c = data['perc_arr']
    array2c = data['perc_arr_mjo_phase'] 


#array1 = data['perc_arr']
#array2 = data['perc_arr_mjo_phase'] 
hi2005 = np.zeros((5,8))
lo2005 = np.zeros((5,8))
hi2013 = np.zeros((5,8))
lo2013 = np.zeros((5,8))
hi2024 = np.zeros((5,8))
lo2024 = np.zeros((5,8))

ind2005hi = [15, 0, 8, 1, 10]
ind2005lo = [22, 31, 19, 23, 39]
ind2013hi = [8, 21, 17, 27, 28]
ind2013lo = [19, 25, 31, 34, 14]
ind2024hi = [13, 0, 12, 34, 1]
ind2024lo = [32, 36, 4, 38, 6]

tmphi = 0
tmplo = 0
for ind in range(0,5):
    print('2005 value of ind is: ',ind)
    hi2005[ind,:] = array2[ind2005hi[ind],:]
    tmphi = hi2005[ind,0]+hi2005[ind,1]+hi2005[ind,2] + tmphi
    print('hi sum of ph 1,2, and 3: ',hi2005[ind,0]+hi2005[ind,1]+hi2005[ind,2])
    lo2005[ind,:] = array2[ind2005lo[ind],:]
    tmplo = lo2005[ind,0]+lo2005[ind,1]+lo2005[ind,2] + tmplo
    print('lo sum of ph 1,2, and 3: ',lo2005[ind,0]+lo2005[ind,1]+lo2005[ind,2])

print('avg hi value for 2005 is: ',tmphi/5,' and lo value for 2005 is: ',tmplo/5)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

tmphi = 0
tmplo = 0
for ind in range(0,5):
    print('2013 value of ind is: ',ind)
    hi2013[ind,:] = array2[ind2013hi[ind],:]
    tmphi = hi2013[ind,0]+hi2013[ind,1]+hi2013[ind,2] + tmphi
    print('hi sum of ph 1,2, and 3: ',hi2013[ind,0]+hi2013[ind,1]+hi2013[ind,2])
    lo2013[ind,:] = array2[ind2013lo[ind],:]
    tmplo = lo2013[ind,0]+lo2013[ind,1]+lo2013[ind,2] + tmplo
    print('lo sum of ph 1,2, and 3: ',lo2013[ind,0]+lo2013[ind,1]+lo2013[ind,2])

print('avg hi value for 2013 is: ',tmphi/5,' and lo value for 2013 is: ',tmplo/5)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

tmphi = 0
tmplo = 0
for ind in range(0,5):
    print('2024 value of ind is: ',ind)
    hi2024[ind,:] = array2[ind2024hi[ind],:]
    tmphi = hi2024[ind,0]+hi2024[ind,1]+hi2024[ind,2] + tmphi
    print('hi sum of ph 1,2, and 3: ',hi2024[ind,0]+hi2024[ind,1]+hi2024[ind,2])
    lo2024[ind,:] = array2[ind2024lo[ind],:]
    tmplo = lo2024[ind,0]+lo2024[ind,1]+lo2024[ind,2] + tmplo
    print('lo sum of ph 1,2, and 3: ',lo2024[ind,0]+lo2024[ind,1]+lo2024[ind,2])

print('avg hi value for 2024 is: ',tmphi/5,' and lo value for 2024 is: ',tmplo/5)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

#print('perc_arr',array1[:])
#print(f"contents are: {array1.shape}")
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('perc_arr',array1[:])
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('perc_arr',array1b[:])
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('perc_arr',array1c[:])
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

print('perc_arr_mjo_phase',array2[:,0])
print(f"contents are: {array2.shape}")

mn2005 = np.mean(array2,axis=0)
mn2013 = np.mean(array2b,axis=0)
mn2024 = np.mean(array2c,axis=0)

print('means of percentage for 2005 are: ',np.mean(array2,axis=0))
print('means of percentage for 2005 are: ',mn2005)
print('means of percentage for 2013 are: ',np.mean(array2b,axis=0))
print('means of percentage for 2024 are: ',np.mean(array2c,axis=0))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('phases 1,2,3, and 8 from 2005: ',mn2005[0],' ',mn2005[1],' ',mn2005[2],' ',mn2005[7])
print('total percentage of phases 1,2, and 3 from 2005: ',mn2005[0]+mn2005[1]+mn2005[2])
print('total percentage of phases 1,2,3, and 8 from 2005: ',mn2005[0]+mn2005[1]+mn2005[2]+mn2005[7])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('phases 1,2,3, and 8 from 2013: ',mn2013[0],' ',mn2013[1],' ',mn2013[2],' ',mn2013[7])
print('total percentage of phases 1,2, and 3 from 2013: ',mn2013[0]+mn2013[1]+mn2013[2])
print('total percentage of phases 1,2,3, and 8 from 2013: ',mn2013[0]+mn2013[1]+mn2013[2]+mn2013[7])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('phases 1,2,3, and 8 from 2024: ',mn2024[0],' ',mn2024[1],' ',mn2024[2],' ',mn2024[7])
print('total percentage of phases 1,2, and 3 from 2024: ',mn2024[0]+mn2024[1]+mn2024[2])
print('total percentage of phases 1,2,3, and 8 from 2024: ',mn2024[0]+mn2024[1]+mn2024[2]+mn2024[7])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('phases from 2005: ',mn2005[:])
print('sum of phases from 2005: ',np.sum(mn2005[:]))
print('phases from 2013: ',mn2013[:])
print('sum of phases from 2013: ',np.sum(mn2013[:]))
print('phases from 2024: ',mn2024[:])
print('sum of phases from 2024: ',np.sum(mn2024[:]))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('hi from 2005: ',hi2005)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

data2plot1 = array2
data2plot2 = array2b
data2plot3 = array2c

#fig, ax = plt.subplots(3, 1)
#ax.plt.subplot(3,1,1)
#ax.plt.imshow(data2plot1, cmap='viridis', interpolation='nearest')
#ax.plt.title('Percentage of time in MJO phases: 2005')
#ax.plt.colorbar(label='Value') # Adds a color bar to indicate scale
#ax.plt.xlabel('MJO Phase')
#ax.plt.ylabel('ensemble number')
#ax.plt.subplot(3,1,2)
#ax.plt.imshow(data2plot2, cmap='viridis', interpolation='nearest')
#ax.plt.subplot(3,1,3)
#ax.plt.imshow(data2plot3, cmap='viridis', interpolation='nearest')
##plt.show()
#fig.savefig('here_say_my.png', dpi=300)

print('shape of data2plot1: ',np.shape(data2plot1))

v1 = 0
v2 = 15
colors='plasma'
#colors='magma'
#colors='viridis'

fig, axs = plt.subplots(1, 3)
#axs.plt.subplot(3,1,1)
ax1=axs[0].imshow(data2plot1, cmap=colors, interpolation='nearest', vmin=v1, vmax=v2)
#axs.plt.title('Percentage of time in MJO phases: 2005')
axs[0].set_title('2005')
#axs.plt.colorbar(label='Value') # Adds a color bar to indicate scale
axs[0].set_xlabel('MJO Phase')
axs[0].set_ylabel('ensemble number')
#axs.plt.subplot(3,1,2)
axs[1].set_title('2013')
ax2=axs[1].imshow(data2plot2, cmap=colors, interpolation='nearest', vmin=v1, vmax=v2)
axs[1].set_xlabel('MJO Phase')
#axs.plt.subplot(3,1,3)
axs[2].set_title('2024')
ax3=axs[2].imshow(data2plot3, cmap=colors, interpolation='nearest', vmin=v1, vmax=v2)
axs[2].set_xlabel('MJO Phase')
cbar = fig.colorbar(ax1, ax=axs[0])
cbar = fig.colorbar(ax2, ax=axs[1])
cbar = fig.colorbar(ax3, ax=axs[2])
cbar.set_label('no more')
#plt.show()
fig.savefig('mjo_heatmap_augsep.png', dpi=300)
#fig.savefig('mjo_heatmap_junnov.png', dpi=300)
