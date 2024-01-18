# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Covered_Water_Surface.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script scans directories to find files named 'chl_oc3.tif', extracts dates from the directory names, and processes these files to analyze water surfaces.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, re, numpy, matplotlib, rasterio, pandas, datetime, matplotlib.ticker
# ----------------------------------------------------------------------------
# Input: Processes 'chl_oc3.tif' files found in a root directory.
# ----------------------------------------------------------------------------
# Output: Likely generates visualizations or summaries of the water surface analysis (details not specified in the initial part of the code).
# ----------------------------------------------------------------------------

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import pandas as pd
from datetime import datetime
import matplotlib.ticker as ticker

# Function to scan all directories and find all files named 'chl_oc3.tif'
def find_tif_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'chl_oc3.tif':
                yield os.path.join(root, file)

# Function to extract the complete date from the directory name
def extract_date_from_path(path):
    # Extract date using regular expression
    match = re.search(r'\d{4}_\d{2}_\d{2}', path)
    return match.group() if match else None

# Function to count non-NaN pixels and calculate the covered water surface area
def calculate_covered_surface(file_path):
    with rasterio.open(file_path) as dataset:
        # Read the dataset's first band
        band1 = dataset.read(1)
        # Count non-NaN pixels
        non_nan_pixels = np.count_nonzero(~np.isnan(band1))
        # Calculate covered water surface area in square kilometers
        covered_surface = non_nan_pixels * ((30/1000) * (30/1000))
        return covered_surface

# Define the root directory
root_directory = "E:/Thesis/Chapter_3/RS_Data/ACOLITE_Outputs"

# Find all 'chl_oc3.tif' files
tif_files = list(find_tif_files(root_directory))

# Initialize lists to hold the dates and covered surface data
dates = []
covered_surfaces = []

for file_path in tif_files:
    #print(file_path)
    date_str = extract_date_from_path(file_path)
    if date_str:
        date = datetime.strptime(date_str, '%Y_%m_%d')
        covered_surface = calculate_covered_surface(file_path)
        dates.append(date)
        covered_surfaces.append(covered_surface)

# Create a DataFrame from the lists
data = pd.DataFrame({'Date': dates, 'Covered Surface': covered_surfaces})

# Sort the DataFrame by date
data.sort_values('Date', inplace=True)

# Normalize the covered surface values by dividing by 6560.227 and convert to percentage
data['Covered Surface'] = (data['Covered Surface'] / 6560.227) * 100

# Group the data by date and sum the covered surfaces for each date
grouped_data = data.groupby('Date')['Covered Surface'].sum().reset_index()

# Extract years for x-axis labels
grouped_data['Year'] = grouped_data['Date'].dt.year

# Find the unique years and their first occurrence to use as x-tick labels
unique_years = grouped_data['Year'].unique()
year_positions = [grouped_data[grouped_data['Year'] == year].index[0] for year in unique_years]

# Define colors and labels based on the folder name ending
def bar_properties_based_on_folder(file_path):
    if file_path.endswith("017030_L2W\chl_oc3.tif"):
        return 'red', 'black', 0.0 , "Available Water Pixels within ROI (from 17/30 Scenes)"
    elif file_path.endswith("018030_L2W\chl_oc3.tif"):
        return 'blue', 'white', 0.00 , "Available Water Pixels within ROI (from 18/30 Scenes)"
    else:
        return 'grey', 'none', 0.2 , "Available Water Pixels within ROI (other scenes)"  # Default color and label

# Initialize a set to keep track of which labels have been used
used_labels = set()

# Plotting
fig, ax = plt.subplots(figsize=(12, 4))

for index, row in grouped_data.iterrows():
    # Find the file path corresponding to the current row's date
    corresponding_file_path = next((file for file in tif_files if datetime.strptime(extract_date_from_path(file), '%Y_%m_%d') == row['Date']), None)
    if corresponding_file_path:
        # Determine the bar color, edgecolor, linewidth, and label based on the folder name
        color, edgecolor, linewidth, label = bar_properties_based_on_folder(corresponding_file_path)
        # Plot the bar with the specified color, edgecolor, and linewidth
        ax.bar(index, row['Covered Surface'], color=color, edgecolor=edgecolor, linewidth=linewidth, label=label if label not in used_labels else "")

# Set the y-axis limit from 0 to 100
ax.set_ylim(0, 100)

# Set xlim to the range of the data
ax.set_xlim(left=0, right=len(grouped_data.index)-1)

# Set the x-axis ticks and labels
ax.set_xticks(year_positions)
ax.set_xticklabels(unique_years)

# Rotate the labels and set font
for label in ax.get_xticklabels():
    label.set_rotation(45)
    label.set_fontsize(12)
    label.set_fontname('Times New Roman')

# Set axis labels with the new y-axis label
plt.xlabel('Year', fontsize=14, fontname='Times New Roman')
plt.ylabel('Percentage (%)', fontsize=14, fontname='Times New Roman')

# Customizing the legend to only show one entry per label
handles, labels = ax.get_legend_handles_labels()
unique_labels_handles = dict(zip(labels, handles)).items()

legend = ax.legend(
    [handle for label, handle in unique_labels_handles],
    [label for label, handle in unique_labels_handles],
    loc='upper right', framealpha=0.75)

for text in legend.get_texts():
    text.set_fontsize(12)
    text.set_fontname('Times New Roman')

# Customizing tick labels for y-axis
for tick in ax.get_yticklabels():
    tick.set_fontsize(12)
    tick.set_fontname('Times New Roman')

plt.tight_layout()

# Save the figure in different formats with a DPI of 1200 for JPEG and EPS
output_dir = "C:/Users/PHYS3009/Desktop/Covered_Water_Surface"
file_name = "Covered_Water_Surface"
os.makedirs(output_dir, exist_ok=True)
base_file_path = os.path.join(output_dir, file_name)
plt.savefig(f'{base_file_path}.svg', format='svg')
plt.show()
