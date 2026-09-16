import xarray as xr
import numpy as np

year = 2020
station     = 'LL12'
station_lat = 59.48350
station_lon = 22.89683

input_fname = '' # add location of input era5 files here
ds = xr.open_mfdataset(input_fname)
ds = ds.sel(latitude=station_lat,method='nearest').sel(longitude=station_lon,method='nearest')
#ds.to_netcdf('era5_{}_{}.nc'.format(station,year))

ds.msdwswrf.to_netcdf('physics/era5_shortwave_{}_{}.nc'.format(station,year))

u_wind = ds.u10
v_wind = ds.v10
wind_speed = np.sqrt(np.square(u_wind)+np.square(v_wind))
wind_speed.to_netcdf('physics/era5_winds_{}_{}.nc'.format(station,year))
