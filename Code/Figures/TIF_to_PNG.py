# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: TIF_to_PNG.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script converts TIF files to PNG format. It includes functionalities for reading raster data, processing it, and saving the output as PNG images.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os, matplotlib, rasterio, geopandas, numpy, PIL, glob
# ----------------------------------------------------------------------------
# Input: Reads TIF files from a specified directory.
# ----------------------------------------------------------------------------
# Output: Saves converted PNG images to a specified location.
# ----------------------------------------------------------------------------

import os
import matplotlib
import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import rasterio.plot
import matplotlib.font_manager as font_manager
from PIL import Image
import matplotlib.animation as animation
import glob


# Define the directories
input_dir = "E:\\Thesis\\Chapter_3\\RS_Data\\Test"
#input_dir = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_Annual"
output_dir = "E:\\Thesis\\Chapter_3\\RS_Data\\Chla_Outputs_PNG"
shapefile_path = "C:\\Users\\PHYS3009\\Desktop\\TIF_to_PNG\\TIF_to_PNG_Shapefile\\wlo_boundaries_shp.shp"

# Load and transform the shapefile to match raster's coordinate system (WKID 32617)
shapefile = gpd.read_file(shapefile_path)
shapefile = shapefile.to_crs(epsg=32617)

# Function to process each TIFF file
def process_tiff(file_path, output_path, date_str, data_str2):
    dpi = 300
    fig_width = 3440 / dpi 
    fig_height = 3090 / dpi

    with rasterio.open(file_path) as src:
        # Create a figure and axis with the specified size
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        # Show the raster data with Viridis colormap
        rasterio.plot.show(src, ax=ax, cmap='viridis', vmin=0, vmax=30)

        # Set the extent to match the shapefile's bounding box
        minx, miny, maxx, maxy = shapefile.total_bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)

        # Overlay the shapefile
        shapefile.plot(ax=ax, edgecolor='black', facecolor='none')

        # Add color bar
        cbar = plt.colorbar(ax.images[0], ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)
        cbar.set_label('Estimated Chl-a (µg/L)', fontname='PrimaSerif BT', fontsize=18)
        cbar.set_ticks(np.arange(0, 31, 5))
        # Set font for color bar tick labels
        for label in cbar.ax.get_xticklabels():
            label.set_fontname('PrimaSerif BT')
            label.set_fontsize(18)

        # Add titles
        title_font = font_manager.FontProperties(family='Prima Serif', style='normal', size=12)
        ax.set_title(f"Acquisition Date: {date_str}\nSensor: {data_str2}\nLocation: Western Lake Ontario & Hamilton Harbour", fontproperties=title_font, fontsize=18, pad=20, loc='left')

        # Load logos
        logo1 = Image.open("C:\\Users\\PHYS3009\\Desktop\\TIF_to_PNG\\TIF_to_PNG_Logos\\WATERLO1-22766-PP-removebg-preview.png")
        logo2 = Image.open("C:\\Users\\PHYS3009\\Desktop\\TIF_to_PNG\\TIF_to_PNG_Logos\\40ed84_4df788ae4ebc4ef9840c71acc6f79996~mv2.png")

        # Resize logos (adjust sizes as needed)
        logo1 = logo1.resize(((66*8), (37*8))) 
        logo2 = logo2.resize((250, 230))

        # Place logos on the plot
        fig.figimage(logo1, 50-70, fig.bbox.ymax + 850+75)
        fig.figimage(logo2, 600-80, fig.bbox.ymax + 865+75) 

        # Remove axis labels and frame
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Save the figure
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)

# Iterate over the directories and files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.tif'):
            year = os.path.basename(root)
            file_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, year, file.replace('.tif', '.png'))

            # Ensure the output directory exists
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            # Correctly extract date from file name
            parts = file.split('_')
            date_str = f"{parts[2]}-{parts[3]}-{parts[4]}"


            # Iterate over the directories and files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.tif'):
            year = os.path.basename(root)
            file_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, year, file.replace('.tif', '.png'))
            # Correctly extract date from file name
            parts = file.split('_')
            date_str = f"{parts[2]}-{parts[3]}-{parts[4]}"

            # Define data_str2 based on the sensor type
            if parts[0] == 'L8':
                data_str2 = 'OLI (Landsat 8)'
            elif parts[0] == 'L9':
                data_str2 = 'OLI-2 (Landsat 9)'
            else:
                data_str2 = 'Unknown Sensor'

            # Process the TIFF file
            process_tiff(file_path, output_path, date_str, data_str2)

print("Image processing complete.")

# Function to sort files by acquisition date (extracted from file name)
# Define dpi globally if used outside process_tiff
dpi = 300

# Function to sort files by acquisition date (extracted from file name)
def sort_key(filename):
    parts = os.path.basename(filename).split('_')
    return f"{parts[2]}-{parts[3]}-{parts[4]}"

# Collect all PNG files from the output directory, sorted by date
png_files = sorted(glob.glob(os.path.join(output_dir, '**', '*.png'), recursive=True), key=sort_key)

# Create a figure for the animation
fig = plt.figure(figsize=(3440 / dpi , 3090 / dpi ))

# Function to update the frame of the animation
def update_frame(i):
    plt.clf()
    plt.imshow(Image.open(png_files[i]))
    plt.axis('off')  # Hide axis

# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=len(png_files), interval=500)  # 500ms per frame

# Save the animation
animation_output_path = os.path.join("E:\\Thesis\Chapter_3\RS_Data\Chla_Outputs_PNG", "animation.mp4")
ani.save(animation_output_path, writer='ffmpeg', dpi=dpi)

print("Animation complete and saved to:", animation_output_path)
                                     
