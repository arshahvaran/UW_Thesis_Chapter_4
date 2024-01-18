# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Bloom_Indicators.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script is designed for processing TIFF files to calculate bloom indicators. It reads TIFF files, converts them to numpy arrays, and performs calculations to determine bloom intensity.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, numpy, pandas, tifffile
# ----------------------------------------------------------------------------
# Input: Reads TIFF files from a specified directory.
# ----------------------------------------------------------------------------
# Output: The script likely generates statistical data on bloom intensity (details not specified in the initial part of the code).
# ----------------------------------------------------------------------------

import os
import numpy as np
import pandas as pd
import tifffile as tiff

def process_tiff_file(file_path):
    try:
        # Read TIFF file
        img = tiff.imread(file_path)
        img_array = np.array(img)

        # Calculating Bloom_Intensity_ugL
        valid_pixels_intensity = img_array[(img_array >= 10.00) & (img_array <= 30.00)]
        Bloom_Intensity_ugL = np.mean(valid_pixels_intensity) if valid_pixels_intensity.size else 0

        # Calculating Bloom_Extent_km2
        Bloom_Extent_km2 = valid_pixels_intensity.size * 0.0009

        # Calculating Bloom_Severity_ugkm2L
        Bloom_Severity_ugkm2L = Bloom_Intensity_ugL * Bloom_Extent_km2

        # Calculating Data_Availibity_%
        total_valid_pixels = img_array[(img_array >= 0.01) & (img_array <= 30.00)]
        Area_HH_km2 = 20.6281
        Area_WLOO_km2 = 5938.660
        Area_WLON_km2 = 600.9387

        #Data_Availibity_percent = (total_valid_pixels.size * 0.0009 * 100) / Area_HH_km2
        #Data_Availibity_percent = (total_valid_pixels.size * 0.0009 * 100) / Area_WLOO_km2
        Data_Availibity_percent = (total_valid_pixels.size * 0.0009 * 100) / Area_WLON_km2

        return [Bloom_Intensity_ugL, Bloom_Extent_km2, Bloom_Severity_ugkm2L, Data_Availibity_percent]

    except Exception as e:
        print(f"Error processing file: {file_path}, Error: {e}")
        return None

def main():
    
    #directory = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_HH"
    #directory = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLOO"
    directory = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLON"

    #output_file = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_HH\\Chla_Outputs_HH.xlsx"
    #output_file = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLOO\\Chla_Outputs_WLOO.xlsx"
    output_file = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLON\\Chla_Outputs_WLON.xlsx"

    data = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tif'):
                file_path = os.path.join(root, file)
                result = process_tiff_file(file_path)
                if result:
                    data.append([file] + result)
                else:
                    print(f"Skipped file: {file}")

    df = pd.DataFrame(data, columns=["File_Name", "Bloom_Intensity_ugL", "Bloom_Extent_km2", "Bloom_Severity_ugkm2L", "Data_Availibity_%"])
    df["Bloom_Intensity_ugL"] = df["Bloom_Intensity_ugL"].round(3)
    df["Bloom_Extent_km2"] = df["Bloom_Extent_km2"].round(3)
    df["Bloom_Severity_ugkm2L"] = df["Bloom_Severity_ugkm2L"].round(3)
    df["Data_Availibity_%"] = df["Data_Availibity_%"].round(1)
    df.to_excel(output_file, index=False)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
