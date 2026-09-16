import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

st     = 'LL12'
year   = 2020

run_id =                                                                                   ['ctrl']#, names of pika-ergom iterations     
dofyr  =                                                                                        22  # day of year - needs to match obs!
units  =                                                                                'mmol m⁻³' # units
var    =                                                                                     'no3' # variable
                                                                                             #^^   !!! Check that variable names match !!!
ds    = xr.open_dataset('init/init_{}_{}.nc'.format(st,year)).isel(time=dofyr).no3  # variable
cmems = np.squeeze(ds.values)
times = ds.time.values
depth = ds.depth.values

plt.figure()

for name in run_id:
    # read in an iteration of pika-ERGOM, and find the closest depth to that requested
    ds         = xr.open_dataarray('{}_{}.nc'.format(name,var)).isel(time=dofyr)
    pika       = np.squeeze(ds.values)
    # note actual depth from file
    pika_depth = ds.depth.values
    # read time axis
    pika_time  = ds.time.dt.strftime("%Y-%m-%d").values
    print(pika_time)
    # plot iteration as time series
    plt.plot(pika,-pika_depth,label='pika-ergom_{}'.format(name))

# plot reanalysis as reference
plt.plot(cmems,-depth,label='cmems-reanalysis')
plt.ylabel('Depth (m)')
plt.xlabel('Nitrate (mmol/m³)')
plt.title('{}'.format(pika_time))
plt.grid()

# plot data points
data_dir  = '' # location where profiles are stored
ds        = xr.open_dataset('{}/{}/netcdf_files/{}_{}_{}.nc'.format(data_dir,st,var,st,year))
obs_val   = ds.no3.values
obs_dpt   = ds.depth.values
obs_times = ds.time.dt.strftime("%Y-%m-%d").values
val_now   = obs_val[obs_times==pika_time]
dpt_now   = obs_dpt[obs_times==pika_time]

# need to sort these
dpt_i = dpt_now.argsort()
dpt_s = dpt_now[dpt_i[0::]]
val_now_s = val_now[dpt_i[0::]]

plt.scatter(val_now/14,-dpt_now,label='obs')

plt.xlim(0,10)
plt.legend()
plt.savefig('profiles_{}_{}.png'.format(var,dofyr))
