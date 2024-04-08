import pandas as pd
import xarray as xr
from functools import reduce


# rain

ds = xr.open_dataset('rainfall_hadukgrid_uk_5km_ann-30y.nc')
rain_df = ds.to_dataframe().reset_index()

rain_df = rain_df.loc[:, ['rainfall', 'latitude', 'longitude']]

rain_df = rain_df.dropna()

rain_df = rain_df.drop_duplicates(keep='first')

# sun

ds = xr.open_dataset('sun_hadukgrid_uk_5km_ann-30y.nc')
sun_df = ds.to_dataframe().reset_index()

sun_df = sun_df.loc[:, ['sun', 'latitude', 'longitude']]

sun_df = sun_df.dropna()

sun_df = sun_df.drop_duplicates(keep='first')

# wind

ds = xr.open_dataset('sfcWind_hadukgrid_uk_5km_ann-30y.nc')
wind_df = ds.to_dataframe().reset_index()

wind_df = wind_df.loc[:, ['sfcWind', 'latitude', 'longitude']]

wind_df = wind_df.dropna()

wind_df = wind_df.drop_duplicates(keep='first')

# surface temp

ds = xr.open_dataset('tas_hadukgrid_uk_5km_ann-30y.nc')
tas_df = ds.to_dataframe().reset_index()

tas_df = tas_df.loc[:, ['tas', 'latitude', 'longitude']]

tas_df = tas_df.dropna()

tas_df = tas_df.drop_duplicates(keep='first')


## snow

ds = xr.open_dataset('snowLying_hadukgrid_uk_5km_ann-30y.nc')
snow_df = ds.to_dataframe().reset_index()

snow_df = snow_df.loc[:, ['snowLying', 'latitude', 'longitude']]

snow_df = snow_df.dropna()

snow_df = snow_df.drop_duplicates(keep='first')

## groundfrost

ds = xr.open_dataset('groundfrost_hadukgrid_uk_5km_ann-30y.nc')
groundfrost_df = ds.to_dataframe().reset_index()

groundfrost_df = groundfrost_df.loc[:, ['groundfrost', 'latitude', 'longitude']]

groundfrost_df = groundfrost_df.dropna()

groundfrost_df = groundfrost_df.drop_duplicates(keep='first')


## hurs humidity

ds = xr.open_dataset('hurs_hadukgrid_uk_5km_ann-30y.nc')
hurs_df = ds.to_dataframe().reset_index()

hurs_df = hurs_df.loc[:, ['hurs', 'latitude', 'longitude']]

hurs_df = hurs_df.dropna()

hurs_df = hurs_df.drop_duplicates(keep='first')

# Merge the dataframes on 'latitude' and 'longitude'

dataframes = [rain_df, sun_df, wind_df, tas_df, snow_df, groundfrost_df, hurs_df]

# use reduce to merge all dataframes on 'latitude' and 'longitude'
merged_df = reduce(lambda left, right: pd.merge(left, right, on=['latitude', 'longitude']), dataframes)

merged_df.to_excel('weatherconditions_with_lat_lon.xlsx', index=False)