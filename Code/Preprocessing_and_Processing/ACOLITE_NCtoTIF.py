# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: ACOLITE_NCtoTIF.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script converts .nc (NetCDF) files to TIF format. It traverses a directory structure, identifies .nc files, and performs the conversion using the GDAL library.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, xarray, osgeo (gdal, osr)
# ----------------------------------------------------------------------------
# Input: Reads .nc files from a specified root folder.
# ----------------------------------------------------------------------------
# Output: Saves the converted TIF files in a new folder.
# ----------------------------------------------------------------------------

import os
import xarray as xr
from osgeo import gdal, osr

def extract_and_save_rasters(root_folder):
    # Traverse through the nested folder structure
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # Check if the file is a .nc file
            if file.endswith(".nc"):
                nc_file_path = os.path.join(root, file)
                # Create a new folder named after the .nc file
                output_folder = os.path.join(root, os.path.splitext(file)[0])
                os.makedirs(output_folder, exist_ok=True)
                
                # Open the .nc file with xarray
                ds = xr.open_dataset(nc_file_path)
                crs_wkt = ds.transverse_mercator.crs_wkt
                
                for var_name in ds.data_vars:
                    # Get the variable (data array)
                    data_array = ds[var_name]
                    # Check the number of dimensions in data_array
                    if len(data_array.shape) >= 2:
                        # Define the .tif file name
                        tif_path = os.path.join(output_folder, f"{var_name}.tif")
                        
                        # Create a GDAL dataset and save the data array to a .tif file
                        driver = gdal.GetDriverByName('GTiff')
                        out_ds = driver.Create(tif_path, data_array.shape[1], data_array.shape[0], 1, gdal.GDT_Float32)
                        out_band = out_ds.GetRasterBand(1)
                        out_band.WriteArray(data_array.values)
                        
                        # Set the CRS from the extracted WKT string
                        srs = osr.SpatialReference()
                        srs.ImportFromWkt(crs_wkt)
                        out_ds.SetProjection(srs.ExportToWkt())
                        
                        # Set the geotransform here (you might need to adjust this part based on the actual geotransform values)
                        out_ds.SetGeoTransform([586260, 30, 0, 4870470, 0, -30])
                        
                        out_ds = None  # Close the dataset to write to disk
                    else:
                        print(f"Skipping variable {var_name} as it has less than 2 dimensions.")

# Call the function, specifying the root folder
extract_and_save_rasters("E:\\Thesis\\Chapter_3\\RS_Data\\ACOLITE_Outputs")

