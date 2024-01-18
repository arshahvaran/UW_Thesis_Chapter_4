# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Cell_Statistics_Monthly.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: Similar to "Cell_Statistics_Annual.py", this script performs cell statistics operations on a monthly basis using the ArcPy library. It includes setting up environment variables and processing raster data for monthly statistics.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: arcpy, os
# ----------------------------------------------------------------------------
# Input: Processes raster data from specified input directories.
# ----------------------------------------------------------------------------
# Output: Outputs monthly cell statistics to defined locations.
# ----------------------------------------------------------------------------

import arcpy
import os

# Set the environment settings
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(32617) 
arcpy.env.extent = '579271.5 4774252.13214014 733018.5 4877647.86785986'

# Base directories
input_base_dir = r"E:\Thesis\Chapter_3\RS_Data\Chla_Outputs_Monthly"
output_base_dir = r"E:\Thesis\Chapter_3\RS_Data\Final_Maps_Monthly"

# Operations to perform
operations = ["MEAN", "MAXIMUM", "STD"]

for month in range(1, 13):
    month_folder = os.path.join(input_base_dir, f"{month:02d}") 
    output_folders = {
        "MEAN": os.path.join(output_base_dir, "Monthly_Avg"),
        "MAXIMUM": os.path.join(output_base_dir, "Monthly_Max"),
        "STD": os.path.join(output_base_dir, "Monthly_Std")
    }

    # List all TIFF files in the month folder
    tif_files = [os.path.join(month_folder, f) for f in os.listdir(month_folder) if f.endswith('.tif')]

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
        output_path = os.path.join(output_folders[op], f"{month:02d}.tif")
        out_raster.save(output_path)

