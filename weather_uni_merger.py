import pandas as pd
from sklearn.neighbors import BallTree
import numpy as np

df_universities = pd.read_excel('NSS23_All_Undergrads_Locations.xlsx')
df_weather = pd.read_excel('weatherconditions_with_lat_lon.xlsx')

# rename column for readiability
df_universities.rename(columns={'lat': 'latitude'}, inplace=True)
df_universities.rename(columns={'lon': 'longitude'}, inplace=True)

# lat and lon of weather stations are universities aren't exact. 
# hence, we gotta find the nearest neighbour

# harvensine requires radians
df_universities['latitude_rad'] = np.radians(df_universities['latitude'])
df_universities['longitude_rad'] = np.radians(df_universities['longitude'])
df_weather['latitude_rad'] = np.radians(df_weather['latitude'])
df_weather['longitude_rad'] = np.radians(df_weather['longitude'])

# create a a ball tree for nearest neighbor queries
# ballTree is a ds that is used to quickly find the nearest neighbors 
# of a point or set of points within a multi-dimensional space i.e. our lat and lon
tree = BallTree(df_weather[['latitude_rad', 'longitude_rad']], metric='haversine')

# query the tree for the closest point to each university
# idx gives index of closest station
_, idx = tree.query(df_universities[['latitude_rad', 'longitude_rad']], k=1)  # k=1 for the closest neighbor

# link between each university and its closest weather station
df_universities['nearest_station_index'] = idx.flatten()

new_df = df_universities.merge(df_weather[['rainfall','sun','sfcWind', 'tas',
                                           'snowLying','groundfrost','hurs']], 
                                          left_on='nearest_station_index', 
                                          right_index=True,
                                          how='left')


columns_to_drop = ['latitude_rad', 'longitude_rad', 'nearest_station_index']

new_df = new_df.drop(columns=columns_to_drop, axis=1)

new_df = new_df.dropna()

new_df.to_excel('universities_with_weather_data.xlsx', index=False)