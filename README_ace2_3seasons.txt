#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# information related to the paper: 
#
# see lgs_080526
#
# create a data directory on maui (/..../.../data/ace2_3seasons/) that contains the critical info.  zip the data
# into a reasonable number of files to then upload to zenodo.  still need to add the data that results from the scripts like 
# calc_rmm_1yr.py...   what exactly is the necessary output data files from that?  
#
# make a git repo with analysis scripts.
#
# all analysis scripts where originally written by either Levi Silvers or Mu-Ting Chien.   
# during some of the later stages of figure creation and analysis github copilot was also 
# used to help verify and troubleshoot results.  
#
# levi silvers                                   September, 2026
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# figures in the submitted version of Silvers_etal_2026

 
# 1.  How are the number of TCs in the ACE2 ensembles counted? 
    # with this script: tc_numPerYear_ace2_public.py
    # however, tc_numPerYear_ace2_public.py takes as input the 10 ensemble member decade files.  
    #
    # the 10 ensemble member files with TC number information are broken 
    # into individual ensemble members with this script: read_1yr_TC_public.py

# 2.  How do I interpolate and split the output from ACE2 into individual ensemble members?
    # precipitation
        # ace2_pp_driver_public.sh   --> the precip variable is pulled from the larger output files and split into single year chunks
        # interp_ace2_precip.py --> each year of the precip data is interpolated to a coarse grid over a particular latitudinal domain
    # wind
        # interp_ace2_public.py      --> interpolates the wind data to a particular domain: e.g. int_u850_2005dec01_yr1-5_pm30.nc --> this needs to be run for every 5 ensemble members:  usage is $$ python interp_ace2_maui.py 4 2024
        # --> the driver script ace2_pp_driver_wind_interp_public.sh was written to simplify/streamline this process a bit.
        # the output from ace2_pp_driver_wind_interp_public.sh (e.g int_u850_2005dec02_yr6-10_*.nc) then needs to be copied to here: 
        # /data/ACE2/, where it can then be split into individual ensemble members using this script: 
        # ace2_pp_driver_wind_public.sh
    # TWP
        # TWP, like precip, is in the large autoregressive_prediction files and needs to be extracted for size manageability. this can 
        # be done with the script: 
        # ace2_pp_driver_public.sh
        #   so where is the TWP interpolated and split into ensemble members? it is here: interp_ace2_TWP.py 

# 3.  How do I process the data for each ensemble member of ACE2?


### calc_rmm_1yr.py...  run this for each season, e.g.  
python calc_rmm_1yr.py 2024

computes the mean percentage of the time spent in favorable MJO phases for quiet and busy ensemble members.   

### ace2_pp_driver_rmm_1yr.sh --> runs find_rmm_1yr.py for all 120 ensembles
# what input does find_rmm_1yr.py need? 
TC_genesis_1yr_2024_dec04_2001.0_ace2.npz
int_prec_2024_dec04_01_b.nc
int_2024_dec04_01_u850_b.nc
int_2024_dec04_01_u200_b.nc
MJO_EOF_ERA5_2001_2010.npz

# what does find_rmm_1yr.py produce?   Many things:
# A one ensemble member figure timeseries of the RMM1 and RMM2 metrics, with the selected MJO phases illustrated in shading
# An 8 panel figure showing maps of the precipitaiton, u200 and u850 winds for each of the 8 phases of the MJO.



### tcNum_mjoPhase_ace2.py 
#--> cycles through all ensemble members for a particular year and then outputs the number of TC genesis events and
#    the percentage of time the MJO spent in a set of phases for each ensemble member.  this data is saved to a 
#    file named output_timeseries.csv

# e.g. syntax
python tcNum_mjoPhase_ace2.py 2013

# what input does tcNum_mjoPhase_ace2.py need?  
# output from tcNum_mjoPhase_ace2.py is a file named output_timeseries.csv

### plot_timeseries_csv.py
# produces a timeseries figure of TC counts and the fraction of time when the MJO fwas in a designated set of phases.

# e.g. syntax (using output from previous script, tcNum_mjoPhase)
python plot_timeseries_csv.py --x-as-index --xtick-step 5 --i output_timeseries.csv

# input plot_timeseries_csv.py needs as input something like this: output_timeseries_2024_AugThSep01_1238.csv
#              input computed in tcNum_mjoPhase_ace2.py

# output: output_timeseries_plot.png --> see the figures S3-S5 in the Supplemental Information document.  

### parse_tc_tracks.py

# e.g. syntax
python parse_tc_tracks.py --split-years /ACE2/TCoutput/dec02/tracks.ACE2.TC.10yr.2005.dec01.txt -o /ACE2/TCoutput/

### compute_tc_daily_counts.py
# this script writes an output txt file that contains the date (the year is wrong, but month and day are correct), 
# the month of occurrance, the number of storms that are present, and the number of storms that begin on that date.

# e.g. syntax
python compute_tc_daily_counts.py /Users/C823281551/data/ACE2/tc_data/tracks.ACE2.TC.10yr.2024.dec04.2008.txt --format txt --basin NATL --start-lat-min -30 --start-lat-max 30

### ave_TCdays.py
python ave_TCdays.py

### plot_MJO_TC_ts_1yr.py
# this script plots the timeseries of RMM1 and RMM2, uses color shading to identify which of the eight 
# phases of the MJO are occurring, and overlays the occurance of TC genesis events.  

# plot_MJO_TC_ts_1yr.py functions on one ensemble member at a time.  

# e.g. syntax (choose desired year, decade, and ensemble number): 
python plot_MJO_TC_ts_1yr.py gah 2024 dec04 02

#4.   Scripts


# 5.  Where is the data stored?  
    # the final data files that are used by find_rmm_1yr.py are here: 
    ace2_3seasons_data/

# 6.  Generation of figures 
	# 6.a  Figure 1 --> background: the rSST figures are made with sst_era5_ace2.jl; also relevant is 
                            # the test_mapHR_era5.jl script
	# 6.b  Figure 2 --> overall distribution/pdfs/violinPlots --> tc_find_tc_gen_ace2.py
                        --> # where was the histogram of tangential wind made?  tc_intensity_ace2.py, needs to be run on maui.  
	# 6.c  Figure 3 --> large-scale environmental parameteres (ace2_climo_complot.py needs to be run for each year)
	# 6.d  Figure 4 --> MJO diagnostics (ace2_mjo_complot.py produces the tc genesis vs mjo phase)
        #               --> also see open_mjophase.py --> generates heatmaps
        #               --> what script calculates the numbers that go into the histogram in figure 4?
        #               --> the histogram is computed in the ace2_TCvsMJO_fig notebook.   But values are not computed in that notebook. 






# i did this: 
zip archive_name.zip int_2013*TWP_b.nc


