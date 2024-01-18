# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Correlation_Matrix.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script is designed for generating a correlation matrix from a specified dataset. It loads data from an Excel file, selects relevant columns, and calculates both Pearson and Spearman correlations. The script merges these correlations into a single matrix, where the upper triangle shows Pearson and the lower triangle shows Spearman correlations. It then visualizes this combined correlation matrix using seaborn and matplotlib.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, numpy, seaborn, matplotlib
# ----------------------------------------------------------------------------
# Input: The script reads data from an Excel file located at "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Matchup_Data_v4.xlsx". It specifically processes columns named 'I1' to 'I8' and 'Log10_Value'.
# ----------------------------------------------------------------------------
# Output: The script outputs a visual representation of the correlation matrix. The plot combines Pearson and Spearman correlations and is visualized using seaborn and matplotlib libraries.
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import matplotlib.patches as patches

# Load the dataset
file_path = "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Matchup_Data_v4.xlsx"
data = pd.read_excel(file_path)

# Selecting the relevant columns
columns = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'Log10_Value']
data = data[columns]

# Calculating Pearson and Spearman correlations
pearson_corr = data.corr(method='pearson')
spearman_corr = data.corr(method='spearman')

# Creating a mask for upper triangle
mask = np.triu(np.ones_like(pearson_corr, dtype=bool))

# Merging Pearson and Spearman correlations
# Upper triangle (including diagonal) will have Pearson, lower triangle will have Spearman
combined_corr = pearson_corr.where(mask, spearman_corr)

# Plotting the correlation matrix
plt.figure(figsize=(10/1.25, 8/1.25))
cmap = sns.diverging_palette(240, 0, s=90, l=50, as_cmap=True)
# Ensuring the color bar ranges from -1 to 1
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)  

heatmap = sns.heatmap(combined_corr, annot=True, fmt=".2f", cmap=cmap, norm=norm, cbar=True, 
            cbar_kws={'label': 'Correlation Coefficient'},
            linewidths=.15, linecolor='black', annot_kws={'size': 10, 'fontname': 'Times New Roman'})

#plt.title("Correlation Matrix\nUpper Triangular: Pearson (r), Lower Triangular: Spearman's Rank (ρ)", fontname='Times New Roman', fontsize=12)
plt.xticks(fontsize=11, fontname="Times New Roman")
plt.yticks(fontsize=11, fontname="Times New Roman")

# Renaming the last label
column_labels = [col if col != 'Log10_Value' else 'Log(Chl-a)' for col in columns]

plt.xticks(ticks=np.arange(len(column_labels)) + .5, labels=column_labels, rotation=45)
plt.yticks(ticks=np.arange(len(column_labels)) + .5, labels=column_labels)

# Adjusting color bar label font and ticks
cbar = heatmap.collections[0].colorbar
cbar.ax.set_ylabel('Correlation Coefficient', fontname='Times New Roman', fontsize=11)

# Get the current locations and set them as fixed locations
locations = cbar.ax.get_yticks()
cbar.ax.yaxis.set_major_locator(plt.FixedLocator(locations))

# Now set the tick labels with the desired font
cbar.ax.set_yticklabels(locations, fontname='Times New Roman', fontsize=11)


# Adding a thick border around the Log10(Chl-a) rows and columns
# Assuming Log10(Chl-a) is the last column and row, adjust index as needed
log10_chla_index = len(columns) - 1  # Index of the Log10(Chl-a) column and row
rect1 = patches.Rectangle((log10_chla_index -8 , log10_chla_index ), 9, 1, linewidth=1.5, edgecolor='black', facecolor='none')
rect2 = patches.Rectangle((log10_chla_index  , log10_chla_index -8), 1, 9, linewidth=1.5, edgecolor='black', facecolor='none')

# Add the rectangle to the plot
plt.gca().add_patch(rect1)
plt.gca().add_patch(rect2)

# Adjust layout
plt.tight_layout()

# Save the figure as an SVG file
plt.savefig("C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Correlation_Matrix\\Correlation_Matrix.svg", format='svg', bbox_inches='tight')

plt.show()
