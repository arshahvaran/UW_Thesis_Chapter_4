# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Reflectance_Comparison_Merged.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script merges several Excel files containing reflectance data. It reads the files, identifies common columns, and performs the merging operation.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas
# ----------------------------------------------------------------------------
# Input: Reads from multiple Excel files located at "C:/Users/PHYS3009/Desktop/Merge".
# ----------------------------------------------------------------------------
# Output: The specific output format is not detailed in the initial part of the code.
# ----------------------------------------------------------------------------

import pandas as pd

# File paths for the Excel files to be merged
file1 = "C:/Users/PHYS3009/Desktop/Merge/Matchup_Data_v2_rhos.xlsx"
file2 = "C:/Users/PHYS3009/Desktop/Merge/Matchup_Data_v2_rhow.xlsx"
file3 = "C:/Users/PHYS3009/Desktop/Merge/Matchup_Data_v2_rhot.xlsx"

# Read the Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
df3 = pd.read_excel(file3)

# Define the common columns for merging
common_columns = ["ID", "Latitude_DD", "Longitude_DD", "Image"]

# Perform the merge
merged_df = df1.merge(df2, on=common_columns, how='outer').merge(df3, on=common_columns, how='outer')

# Drop duplicate columns
merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

# Save the merged DataFrame to a new Excel file
output_file = "C:/Users/PHYS3009/Desktop/Merge/Reflectance_Comparison_Merged.xlsx"
merged_df.to_excel(output_file, index=False)

print(f"Merged file created at {output_file}")
