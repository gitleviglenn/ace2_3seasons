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

# calc_rmm_1yr.py...  run this for each season, e.g.  
python calc_rmm_1yr.py 2024

computes the mean percentage of the time spent in favorable MJO phases for quiet and busy ensemble members.   


# 4.  How much space do the 120 ensemble members need for storage? 

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


