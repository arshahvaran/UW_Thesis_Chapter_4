# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: ACOLITE_Pixel_Extraction_rhow.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script is designed for extracting remote sensing data from raster files. It maps column names to specific raster file names, adjusts mappings for different sensors (L8 and L9), and includes functions for transforming image data. The script is likely used for processing satellite imagery data, particularly focusing on specific wavelengths represented in the raster files.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, pandas, fnmatch, rasterio, pyproj, numpy
# ----------------------------------------------------------------------------
# Input: The script processes raster files (e.g., 'rhow_443.tif', 'rhow_483.tif') located in a specified directory. It likely reads data from these files to perform its operations.
# ----------------------------------------------------------------------------
# Output: The specific output of the script is not directly indicated in the initial part of the code. However, it may involve generating transformed data or summaries based on the input raster files.
# ----------------------------------------------------------------------------

import os
import pandas as pd
import fnmatch
import rasterio
from rasterio.warp import transform
from pyproj import Proj
import numpy as np
from pyproj import Transformer

# Define the mapping for column names to file names
raster_file_mapping = {
    "rhow_443": "rhow_443.tif",
    "rhow_483": "rhow_483.tif",  # This is the default for L8
    "rhow_561": "rhow_561.tif",
    "rhow_655": "rhow_655.tif",  # This is the default for L8
    "rhow_865": "rhow_865.tif",
}

# Adjust the mapping for L9 sensor
raster_file_mapping_L9 = raster_file_mapping.copy()
raster_file_mapping_L9["rhow_483"] = "rhow_482.tif"  # L9 specific file name
raster_file_mapping_L9["rhow_655"] = "rhow_654.tif"  # L9 specific file name

def image_to_folder(image):
    parts = image.split('_')
    sensor = 'L8' if parts[0] == 'LC08' else 'L9' if parts[0] == 'LC09' else None
    date = parts[3][:4] + '_' + parts[3][4:6] + '_' + parts[3][6:]
    return f"{sensor}_OLI_{date}_*_{parts[2]}_L2W"

from pyproj import Transformer

def get_pixel_value(raster_path, lon, lat):
    with rasterio.open(raster_path) as src:
        # Create a transformer object for coordinate transformation
        transformer = Transformer.from_crs("epsg:4326", src.crs, always_xy=True)
        # Perform the transformation
        x, y = transformer.transform(lon, lat)
        
        # Get row and col indices
        row, col = src.index(x, y)
        data = src.read(1)  # Read the first band

        # Initialize a list to collect pixel values
        pixel_values = []

        # Iterate over the 3x3 grid
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                # Calculate the new row and col positions
                new_row, new_col = row + d_row, col + d_col
                if (0 <= new_row < src.height) and (0 <= new_col < src.width):
                    # Get the pixel value at the new position
                    pixel_value = data[new_row, new_col]
                    # If pixel value is not NaN, append to list
                    if not np.isnan(pixel_value):
                        pixel_values.append(pixel_value)
        
        # Calculate the average if there are valid pixels
        if pixel_values:
            return np.mean(pixel_values)
        else:
            return None  # Return None if no valid pixels are found

# Base directory where the folders are located
base_dir = "E:\\Thesis\\Chapter_3\\RS_Data\\ACOLITE_Outputs"

# Reading the Excel file
df = pd.read_excel("C:\\Users\\PHYS3009\\Desktop\\ACOLITE_Pixel_Extraction_rhow\Matchup_Data_v1.xlsx")

# Adding new columns for the raster values
raster_columns = ["rhow_443", "rhow_483", "rhow_561", "rhow_655", "rhow_865"]
for column in raster_columns:
    df[column] = np.nan

# Iterate over the dataframe
for index, row in df.iterrows():
    image_val = row['Image']
    folder_name_pattern = image_to_folder(image_val)
    
    # Determine which set of raster file names to use based on the sensor
    current_raster_mapping = raster_file_mapping_L9 if 'L9' in folder_name_pattern else raster_file_mapping

    # Search for corresponding directory
    for root, dirs, files in os.walk(base_dir):
        for dirname in dirs:
            if fnmatch.fnmatch(dirname, folder_name_pattern):
                directory_path = os.path.join(root, dirname)
                # Extract pixel values for each raster
                for column_name in raster_columns:
                    # Use the mapping to get the correct file name
                    raster_file_name = current_raster_mapping[column_name]
                    raster_path = os.path.join(directory_path, raster_file_name)
                    if os.path.exists(raster_path):
                        value = get_pixel_value(raster_path, row['Longitude_DD'], row['Latitude_DD'])
                        df.at[index, column_name] = value
                break

# Save the dataframe to a new Excel file
output_file = "C:\\Users\\PHYS3009\\Desktop\\ACOLITE_Pixel_Extraction_rhow\Matchup_Data_v2.xlsx"
df.to_excel(output_file, index=False)
