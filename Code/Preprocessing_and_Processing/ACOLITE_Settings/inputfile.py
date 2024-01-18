# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: inputfile.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script is designed to find directories containing .TIF files and writes these directory paths to an output file. It traverses a root directory, identifies relevant directories, and records them.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: os
# ----------------------------------------------------------------------------
# Input: Scans a root directory for .TIF files.
# ----------------------------------------------------------------------------
# Output: Writes the list of directories containing .TIF files to an output file.
# ----------------------------------------------------------------------------


import os

def find_tif_directories(root_dir):
    tif_dirs = []
    
    # Traverse the root directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Look for .tif files in the current directory
        if any(filename.endswith('.TIF') for filename in filenames):
            tif_dirs.append(dirpath)
            
    return tif_dirs

def write_directories_to_file(directories, output_file):
    # Writing the directories to the output file separated by commas
    with open(output_file, 'w') as file:
        file.write(','.join(directories))

# Loop over the years from 2013 to 2023
for year in range(2013, 2024):
    # Root directory to start the search
    root_dir = f"E:\\Thesis\\Chapter_3\\RS_Data\\Level_1\\{year}"

    # Output file to write the directories containing .tif files
    output_file = f"C:\\Users\\PHYS3009\\Desktop\\acolite_py_win_20231023.0\\Python\\inputfile{year}.txt"

    # Finding directories containing .tif files
    tif_directories = find_tif_directories(root_dir)

    # Writing the directories to the output file
    write_directories_to_file(tif_directories, output_file)
