#!/bin/python3

'''
 Extract the TEMIS UV index or UV dose data for a given location.
 
 From a 'europe' file extraction takes a few seconds,
 from a 'world' file extraction may take some 30 seconds.
 
 usage:  uvnctimeseries.py -h
 
 source: https://www.temis.nl/uvradiation/
 
'''

import numpy as np
import netCDF4
import sys
import os

import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# ==================================================================

def GetTimeSeries(lon,lat,ilon,ilat,ncFile):
    '''
     Extract the times series for the selected location, using the
     grid cell indices determined in 'CheckCoordinates'.
    '''
    
    with netCDF4.Dataset(ncFile,'r') as nc:
        
        # Basics of the data
        # ------------------
        
        # What is the geographic coverage?
        # 'World' or 'Europe'
        
        coverage = nc.data_geo_coverage
        
        # What data are we dealing with?
        # 'Daily data' or 'Daily climatology'
        
        dataDescription = nc.data_description
        dataType = dataDescription.split()[1]   # 'data' or 'climatology'
        
        # Is the data UV index or UV dose?
        # 'Erythemal UV index & ozone column'
        # 'Erythemal UV dose cloud-free & cloud-modified'
        # 'Vitamin-D UV dose cloud-free & cloud-modified'
        # 'DNA-damage UV dose cloud-free & cloud-modified'
        
        dataProduct = nc.data_product 
        dataKind = dataProduct.split()[2]  # 'index' or 'dose'
        
        # What period does the data cover?
        # Either a single year (e.g. '2020') or the
        # data period of the climatoloy (e.g. '2004-2020')
        
        dataPeriod = nc.data_period
        
        # Number of data points:
        
        days  = nc.groups['PRODUCT'].variables['days'][:]
        dates = nc.groups['PRODUCT'].variables['date'][:]
        nDays = len(dates)
        
        # If you only need a part of the data, e.g. for testing,
        # fix nDays manually:
        
       # nDays = 100
        
        # Grid cell coordinates 
        
        lons = nc.groups['PRODUCT'].variables['longitude'][:]
        lats = nc.groups['PRODUCT'].variables['latitude'][:]
        
        
        # Read the two main datasets
        # --------------------------
        # This depends on dataType & dataKind.
        # Other datasets can be added accordingly.
        
        if ( dataKind == 'index' ):
            
            data1Str = 'UV index     [-]'
            data2Str = 'Ozone column [DU]'
            
            if ( dataType == 'data' ):
                
                data1 = nc.groups['PRODUCT'].variables['uvi_clear'][0:nDays,ilat,ilon]
                data2 = nc.groups['PRODUCT'].variables['ozone_column'][0:nDays,ilat,ilon]
                format = '  %3d  %8d   %6.3f  %6.1f'
                dateFmt = 'YYYYMMDD'
                
            else: # dataType == 'climatology'
                
                data1 = nc.groups['PRODUCT'].variables['uvi_clear_mean'][0:nDays,ilat,ilon]
                data2 = nc.groups['PRODUCT'].variables['ozone_column_mean'][0:nDays,ilat,ilon]
                format = '  %3d  %04.4d   %6.3f  %6.1f'
                dateFmt = 'MMDD'
                
        else:  # dataKind == 'dose' )
            
            data1Str = 'UV dose cloud-free     [kJ/m2]'
            data2Str = 'UV dose cloud-modified [kJ/m2]'
            
            if ( dataType == 'data' ):
                
                data1 = nc.groups['PRODUCT'].variables['uvd_clear'][0:nDays,ilat,ilon]
                data2 = nc.groups['PRODUCT'].variables['uvd_cloudy'][0:nDays,ilat,ilon]
                format = '  %3d  %8d   %6.3f  %6.3f'
                dateFmt = 'YYYYMMDD'
                
            else: # dataType == 'climatology'
                
                data1 = nc.groups['PRODUCT'].variables['uvd_clear_mean'][0:nDays,ilat,ilon]
                data2 = nc.groups['PRODUCT'].variables['uvd_cloudy_mean'][0:nDays,ilat,ilon]
                format = '  %3d  %04.4d   %6.3f  %6.3f'
                dateFmt = 'MMDD'
    
    # Replace masked values by the literal FillValue ('no data'):
    
    data1 = np.ma.where(data1.mask,-1.0,data1)
    data2 = np.ma.where(data2.mask,-1.0,data2)
    
            
    # Output the data
    # ---------------
    # Here we write in a ascii data format that is
    # suitable for plotting with e.g. Gnuplot.
    
    print('# TEMIS UV data timeseries')
    print('# ========================')
    print('# source: https://www.temis.nl/uvradiation/')
    print('# (c) KNMI/ESA')
    print('#')
    print('# Data product    : %s' % (dataProduct) )
    print('# data type       : %s' % (dataDescription) )
    print('# Data period     : %s' % (dataPeriod) )
    print('#')
    print('# Given location  : lon, lat = %g, %g' % (lon,lat) )
    print('# Grid cell centre: lon, lat = %g, %g' % (lons[ilon],lats[ilat]) )
    print('#')
    print('# No-data entry   : -1.000')
    print('#')
    print('# Data columns:')
    print('#    1 : number of the day in the year')
    print('#    2 : date in the format %s' % (dateFmt) )
    print('#    3 : %s' % (data1Str) )
    print('#    4 : %s' % (data2Str) )
    print('#')
    print('# Dnr  '+dateFmt+'    data1   data2')
    
    for iDay in range(0,nDays,1):
        print(format % ( days[iDay],dates[iDay],data1[iDay],data2[iDay] ) )
     
    return

# ======================           

def CheckCoordinates(lon,lat,ncFile):
    '''
     Make sure that the given coordinate is available within the file,
     which either covers 'world' or 'europe'.
     
     It returns the grid cell indices to use in the data extraction,
     taking the data coverage into account.
    '''
    
    with netCDF4.Dataset(ncFile,'r') as nc:
        
        # The data coverage is specified by global attributes:
        
        lon_min = nc.geospatial_lon_min
        lon_max = nc.geospatial_lon_max 
        lat_min = nc.geospatial_lat_min 
        lat_max = nc.geospatial_lat_max
        
        if ( lon > lon_max  or  lon < lon_min ):
            print(' *** Error: longitude should be in the range [%s:%s]' % (lon_min,lon_max) )
            sys.exit(1)
        
        if ( lat > lat_max  or  lat < lat_min ):
            print(' *** Error: latitude should be in the range [%s:%s]' % (lat_min,lat_max) )
            sys.exit(1)
        
        # Find the offset index of both coordinates;
        # for data that covers the 'world' both are zero.
        
        ilon_offset = nc.groups['PRODUCT'].variables['longitude_index'][0]
        ilat_offset = nc.groups['PRODUCT'].variables['latitude_index'][0]
        
        lons = nc.groups['PRODUCT'].variables['longitude'][:]
        lats = nc.groups['PRODUCT'].variables['latitude'][:]
    
    # Grid cell indices including the
    
    ilon = getIlon(lon) - ilon_offset
    ilat = getIlat(lat) - ilat_offset
    
    return ilon, ilat

# ==================================================================

# Conversion routines of latitude and longitude coordinates in degrees
# to grid cell indices. The index counting is 0-based, that is:
# * longitudes range from 0 (West) to 1439 (East)
# * latitudes  range from 0 (South) to 719 (North)
# and thus covers the full world.
# The grid cells are dlon by dlat = 0.25 by 0.25 degrees

def getIlon(lon):
    dlon = 360.0/1440.0
    return round( ( lon + 180.0 - dlon/2.0 ) / dlon )
def getIlat(lat):
    dlat = 180.0/720.0
    return round( ( lat +  90.0 - dlat/2.0 ) / dlat )
def getLon(ilon):
    dlon = 360.0/1440.
    return dlon * ilon - 180.0 + dlon/2.0
def getLat(ilat):
    dlat = 180.0/720.0
    return dlat * ilat -  90.0 + dlat/2.0

# ==================================================================
# Main part
# ==================================================================

if __name__ == "__main__":
    
    # Configuration
    # -------------
    
    import argparse
    
    dataUrl = "https://www.temis.nl/uvradiation/UVarchive/uvncfiles.php"
    
    parser = argparse.ArgumentParser(description=\
       'Extract the TEMIS UV index or UV dose data for a given location ' +\
       'from a either a file with one year or data or a climatology file, ' +\
       'which can be downloaded from %s || The output is written to the screen.' % (dataUrl) )
    
    lonStr = 'longitude, decimal degrees in range [-180:+180]  '
    parser.add_argument('lon',metavar='LON',help=lonStr)
    
    latStr = 'latitude, decimal degrees in range [-90:+90]'
    parser.add_argument('lat',metavar='LAT',help=latStr)
    
    fileStr = 'netCDF file with the UV index or UV dose data'
    parser.add_argument('file',metavar='FILE',help=fileStr)
    
    args = parser.parse_args()
    
    # Check arguments
    # ---------------
    
    # Check whether the given data file exists
    
    ncFile = args.file
    
    if ( not os.path.isfile(ncFile) ):
        print(' *** Error: given netCDF file does not exist' )
        sys.exit(1)
    
    # Check given coordinates and retrieve grid cell indices to use
    # for the geographic region covered by the data in the file.
    
    lon = float(args.lon)
    lat = float(args.lat)
    
    ilon, ilat = CheckCoordinates(lon,lat,ncFile)
    
    # Retrieve the time series
    # ------------------------
    # Output is written to the screen.
    
    GetTimeSeries(lon,lat,ilon,ilat,ncFile)
    
    # All done
    # --------
    
    sys.exit(0)
    
