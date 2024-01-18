# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Cell_Statistics_Annual.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script uses the ArcPy library to perform cell statistics operations on an annual basis. It sets environment settings for spatial references and extents, and processes raster data to generate annual statistics.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: arcpy, os
# ----------------------------------------------------------------------------
# Input: Processes raster data from specified input directories.
# ----------------------------------------------------------------------------
# Output: Generates annual cell statistics, saved in specified output directories.
# ----------------------------------------------------------------------------

import arcpy
import os

# Set the environment settings
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(32617) 
arcpy.env.extent = '579271.5 4774252.13214014 733018.5 4877647.86785986'

# Base directories
input_base_dir = r"E:\Thesis\Chapter_3\RS_Data\Chla_Outputs"
output_base_dir = r"E:\Thesis\Chapter_3\RS_Data\Final_Maps_Annual"

# Operations to perform
operations = ["MEAN", "MAXIMUM", "STD"]

for year in range(2013, 2024):
    year_folder = os.path.join(input_base_dir, str(year))
    output_folders = {
        "MEAN": os.path.join(output_base_dir, "Annual_Avg"),
        "MAXIMUM": os.path.join(output_base_dir, "Annual_Max"),
        "STD": os.path.join(output_base_dir, "Annual_Std")
    }

    # List all TIFF files in the year folder
    tif_files = [os.path.join(year_folder, f) for f in os.listdir(year_folder) if f.endswith('.tif')]

    for op in operations:
        out_raster = arcpy.sa.CellStatistics(
            in_rasters_or_constants=tif_files,
            statistics_type=op,
            ignore_nodata="DATA",
            process_as_multiband="SINGLE_BAND",
            percentile_value=90,
            percentile_interpolation_type="AUTO_DETECT"
        )

        # Set NoData value to None
        out_raster = arcpy.sa.SetNull(out_raster, out_raster, "VALUE = 0")

        # Save the output
        output_path = os.path.join(output_folders[op], f"{year}.tif")
        out_raster.save(output_path)

