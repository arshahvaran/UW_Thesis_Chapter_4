# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Band_Math.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script processes raster data using band mathematics. It involves reading raster files, applying mathematical operations, and handling concurrent processing.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, rasterio, numpy, concurrent.futures, logging
# ----------------------------------------------------------------------------
# Input: Processes raster data, specifically handling exceptions for certain folders.
# ----------------------------------------------------------------------------
# Output: The specific output format is not detailed in the initial part of the code.
# ----------------------------------------------------------------------------

import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import logging

# Setup logging
logging.basicConfig(filename='chl-a_processing.log', level=logging.INFO)

skip_folders = [
                "L8_OLI_2013_06_22_15_59_31_017030_L2W",
                "L8_OLI_2013_06_13_16_05_47_018030_L2W",
                "L8_OLI_2014_12_02_15_57_48_017030_L2W",
                "L8_OLI_2014_11_16_15_57_49_017030_L2W",
                "L8_OLI_2014_05_08_15_57_13_017030_L2W",
                "L8_OLI_2015_01_26_16_03_45_018030_L2W",
                "L8_OLI_2015_05_11_15_56_40_017030_L2W",
                "L8_OLI_2015_10_02_15_57_38_017030_L2W",
                "L8_OLI_2015_11_26_16_03_57_018030_L2W",
                "L8_OLI_2016_01_22_15_57_42_017030_L2W",
                "L8_OLI_2017_12_17_16_03_58_018030_L2W",
                "L8_OLI_2017_12_10_15_57_45_017030_L2W",
                "L8_OLI_2017_11_15_16_04_02_018030_L2W",
                "L8_OLI_2017_10_23_15_57_55_017030_L2W",
                "L8_OLI_2017_10_14_16_04_05_018030_L2W",
                "L8_OLI_2017_07_26_16_03_43_018030_L2W",
                "L8_OLI_2017_07_10_16_03_36_018030_L2W",
                "L8_OLI_2017_04_30_15_56_54_017030_L2W",
                "L8_OLI_2018_09_08_15_57_12_017030_L2W",
                "L8_OLI_2018_06_20_15_56_34_017030_L2W",
                "L8_OLI_2018_04_24_16_03_01_018030_L2W",
                "L8_OLI_2018_01_27_15_57_32_017030_L2W",
                "L8_OLI_2019_11_30_15_57_56_017030_L2W",
                "L8_OLI_2019_11_05_16_04_10_018030_L2W",
                "L8_OLI_2019_05_22_15_57_15_017030_L2W",
                "L8_OLI_2020_04_29_16_03_16_018030_L2W",
                "L8_OLI_2020_10_15_15_57_57_017030_L2W",
                "L8_OLI_2020_11_07_16_04_05_018030_L2W",
                "L9_OLI_2021_11_12_15_58_41_017030_L2W",
                "L8_OLI_2021_07_21_16_03_45_018030_L2W",
                "L8_OLI_2022_01_22_15_57_47_017030_L2W",
                "L8_OLI_2022_03_11_15_57_35_017030_L2W",
                "L8_OLI_2022_05_05_16_03_38_018030_L2W",
                "L8_OLI_2022_06_06_16_03_52_018030_L2W",
                "L8_OLI_2022_10_12_16_04_18_018030_L2W",
                "L8_OLI_2022_10_28_16_04_26_018030_L2W",
                "L9_OLI_2022_03_10_16_03_49_018030_L2W",
                "L9_OLI_2022_05_06_15_57_18_017030_L2W",
                "L9_OLI_2022_11_05_16_04_13_018030_L2W",
                "L9_OLI_2023_01_01_15_58_04_017030_L2W",
                "L8_OLI_2023_05_08_16_03_09_018030_L2W",
                "L8_OLI_2023_04_06_16_03_27_018030_L2W"
]

def process_image(folder_path):
    try:
        # Define file names based on Landsat version
        folder_name = os.path.basename(folder_path)
        # Skip processing if the folder is in the skip list
        if folder_name in skip_folders:
            logging.info(f"Skipping folder {folder_name}")
            return

        blue_band_name = "rhow_483.tif" if folder_name.startswith("L8") else "rhow_482.tif"
        red_band_name = "rhow_655.tif" if folder_name.startswith("L8") else "rhow_654.tif"

        # Construct file paths
        blue_band_path = os.path.join(folder_path, blue_band_name)
        red_band_path = os.path.join(folder_path, red_band_name)

        # Read the blue and red bands
        with rasterio.open(blue_band_path) as blue_src, rasterio.open(red_band_path) as red_src:
            blue_band = blue_src.read(1, out_dtype='float64')
            red_band = red_src.read(1, out_dtype='float64')

            # Calculate Chl-a
            chl_a = np.where((blue_band == 0) | (red_band == 0), np.nan, 
                             ((10 ** (1.48 * 10 ** (-0.3 * (blue_band / red_band))))-1))

            # Truncate to 1 decimal places
            chl_a = np.around(chl_a, decimals=1)

            # Copy metadata and update
            meta = blue_src.meta
            meta.update(dtype=rasterio.float64, nodata=np.nan)

            # Save the output
            output_folder = os.path.basename(folder_path).split('_')[2] 
            output_path = os.path.join("E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs", output_folder)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            output_file = os.path.join(output_path, os.path.basename(folder_path) + ".tif")
            with rasterio.open(output_file, 'w', **meta) as dst:
                dst.write(chl_a, 1)

            logging.info(f"Processed {folder_path} successfully.")

    except Exception as e:
        logging.error(f"Error processing {folder_path}: {e}")

def main():
    base_dir = "E:\\Thesis\\Chapter_3\\RS_Data\\ACOLITE_Outputs"
    
    # Find all directories ending with 'L2W'
    l2w_folders = [os.path.join(dp, f) for dp, dn, filenames in os.walk(base_dir) 
                   for f in dn if f.endswith('L2W')]
    
    # Process each folder in parallel
    with ProcessPoolExecutor() as executor:
        executor.map(process_image, l2w_folders)

if __name__ == "__main__":
    main()
