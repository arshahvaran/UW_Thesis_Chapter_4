# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Clip.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script uses the ArcPy library to clip raster data using specified shapefiles. It sets the ArcGIS Pro workspace and defines paths for shapefiles used for clipping.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: arcpy, os
# ----------------------------------------------------------------------------
# Input: Uses raster data and shapefiles from specified paths.
# ----------------------------------------------------------------------------
# Output: The script likely outputs clipped raster data (details not specified in the initial part of the code).
# ----------------------------------------------------------------------------

import arcpy
import os

# Set the workspace (change this to your ArcGIS Pro environment path)
arcpy.env.workspace = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs"

# Shapefile paths
shapefiles = {
    "WLON": "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Clip\\WLON_Shapefile\\WLON.shp"
}
    #"HH": "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Clip\\HH_Shapefile\\HH.shp",
    #"WLOO": "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Clip\\WLOO_Shapefile\\WLOO.shp",
    #"WLON": "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Clip\\WLON_Shapefile\\WLON.shp"


# Output directories
output_dirs = {
    "WLON": "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLON"
}

    #"HH": "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_HH",
    #"WLOO": "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLOO",
    #"WLON": "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_WLON"


# Debugging - Check if workspace is correct
print(f"Workspace: {arcpy.env.workspace}")
print(f"Directories in workspace: {os.listdir(arcpy.env.workspace)}")

# Iterate through each subfolder
for year_folder in os.listdir(arcpy.env.workspace):
    year_path = os.path.join(arcpy.env.workspace, year_folder)
    if os.path.isdir(year_path):
        print(f"Processing directory: {year_path}")

        # Process each TIFF file in the subfolder using os.listdir
        for tiff_file in os.listdir(year_path):
            if tiff_file.lower().endswith(".tif"):
                tiff_path = os.path.join(year_path, tiff_file)
                print(f"Processing TIFF file: {tiff_path}")

                for key, shapefile in shapefiles.items():
                    try:
                        # Create output folder for the year if it doesn't exist
                        output_year_folder = os.path.join(output_dirs[key], year_folder)
                        if not os.path.exists(output_year_folder):
                            os.makedirs(output_year_folder)
                            print(f"Created folder: {output_year_folder}")

                        # Set output file path
                        output_file = os.path.join(output_year_folder, os.path.splitext(tiff_file)[0] + f"_{key}.tif")

                        # Execute clipping
                        arcpy.management.Clip(tiff_path, "", output_file, shapefile, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
                        print(f"Output saved to: {output_file}")
                    except Exception as e:
                        print(f"Error processing {tiff_path} with {shapefile}: {e}")

print("Processing complete.")