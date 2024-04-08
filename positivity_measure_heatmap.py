import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.image import imread
from matplotlib.colors import LinearSegmentedColormap

# read in NSS data
data_filepath = os.path.join(os.getcwd(), 'NSS23_Summary_Registered_Full-time.xlsx')
full_df = pd.read_excel(data_filepath, sheet_name=2, skiprows=3)
nss_data = full_df[['Provider name', 'Positivity measure (%)']].copy()

# get average positivity for each provider in NSS data
uni_positivity = nss_data.groupby('Provider name')['Positivity measure (%)'].mean().reset_index()

# get uni location data
data_filepath = os.path.join(os.getcwd(), 'uk_universities_locations.csv')
location_data = pd.read_csv(data_filepath)

df = pd.merge(location_data, uni_positivity, left_on='Name', right_on='Provider name', how='inner')

# define the bin size for latitude and longitude
bin_size = 0.1  
lat_start = 50
lat_stop = 58
lon_start = -7
lon_stop = 2

# create bins
lat_bins = np.arange(lat_start, lat_stop + bin_size, bin_size)
lon_bins = np.arange(lon_start, lon_stop + bin_size, bin_size)

#assign each latitude and longitude to a bin
df['lat_bin'] = np.digitize(df['lat'], bins=lat_bins)
df['lon_bin'] = np.digitize(df['lon'], bins=lon_bins)

# calculate the average positivity measure for each bin
binned_data = df.groupby(['lat_bin', 'lon_bin'])['Positivity measure (%)'].mean().reset_index()

# fill in empty lat_bin lon_bin values
for lat in range(len(lat_bins)):
    for lon in range(len(lon_bins)):
        if not (((binned_data['lat_bin'] == lat) & (binned_data['lon_bin'] == lon)).any()):
            new_record = pd.DataFrame([[lat, lon, np.NaN]], columns=['lat_bin', 'lon_bin', 'Positivity measure (%)'])
            binned_data = pd.concat([binned_data, new_record], ignore_index=True)

# pivot to create a matrix for heatmap plotting
heatmap_data = binned_data.pivot(index='lat_bin', columns='lon_bin', values='Positivity measure (%)')

# Load the map image
map_img = imread('map_of_uk-1.jpg')

# Plot using seaborn with the map as a background
plt.figure(figsize=(14, 12))
# this is going to look different on everyone's screen because of resolution and aspect ratio
plt.imshow(map_img, extent=[-47, 100, -8, 100], aspect='equal')

# customisng the colour map to be orange to blue
colours = ["orange", "blue"]  # 'orange' for low, 'blue' for high
cmap = LinearSegmentedColormap.from_list("custom_orange_blue", colours)

# plot heatmap data on top of the map
sns.heatmap(heatmap_data, cmap=cmap, alpha=1, square=True, cbar_kws={'label': 'Positivity measure (%)'})

# modifying the colour bar
colour_bar = plt.gca().collections[0].colorbar
# move ticks to LHS
colour_bar.ax.yaxis.set_tick_params(labelleft=True, labelright=False)
colour_bar.ax.tick_params(labelsize=14)
# add padding to label so text ins't inside it  
colour_bar.ax.yaxis.labelpad = 20
colour_bar.set_label('Positivity measure (%)', size=16, rotation=270)  


# prevent clutter
tick_frequency = 10
x_tick_labels = [round(lon_start + bin * bin_size, 1) 
                 for bin in range(len(lon_bins)) if bin % tick_frequency == 0]
x_tick_positions = [bin for bin in range(len(lon_bins)) if bin % tick_frequency == 0]

y_tick_labels = [round(lat_start + bin * bin_size, 1) 
                 for bin in range(len(lat_bins)) if bin % tick_frequency == 0]
y_tick_positions = [bin for bin in range(len(lat_bins)) if bin % tick_frequency == 0]

plt.xticks(x_tick_positions, x_tick_labels, fontsize=16)
plt.yticks(y_tick_positions, y_tick_labels, fontsize=16, rotation=360)

plt.gca().set_aspect('equal', adjustable='box')
plt.title('Average Positivity Measure by Location', fontsize=20)
plt.xlabel('Longitude', fontsize=18)
plt.ylabel('Latitude', fontsize=18)

# otherwise it plots the UK upside down
plt.gca().invert_yaxis()

plt.grid()

plt.show()
