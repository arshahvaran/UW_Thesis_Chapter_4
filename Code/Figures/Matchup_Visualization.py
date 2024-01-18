# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Matchup_Visualization.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script visualizes data from an Excel file using matplotlib. It specifically creates a box plot for the given dataset.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, matplotlib
# ----------------------------------------------------------------------------
# Input: Reads data from "Matchup_Data_v3.xlsx" located at 'C:/Users/PHYS3009/Desktop/Matchup_Visualization'.
# ----------------------------------------------------------------------------
# Output: Produces a box plot visualization of the dataset.
# ----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D

# Load the data from the Excel file
file_path = 'C:/Users/PHYS3009/Desktop/Matchup_Visualization/Matchup_Data_v3.xlsx'
data = pd.read_excel(file_path)

# Create the box plot
fig, ax = plt.subplots(figsize=(6, 6))

# Define box properties (borders) and median properties
boxprops = {'color': 'black', 'linewidth': 1.0}
medianprops = {'color': "black", 'linewidth': 0.75}
whiskerprops = {'color': 'black', 'linewidth': 1.0}  # Set whisker color to black
flierprops = {'marker': 'o', 'markerfacecolor': 'black', 'markersize': 3}  # Set outliers to dots

# Plotting the box plot with boxprops and medianprops
data.boxplot(column='Value', by='Study_Area', ax=ax, boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, flierprops=flierprops, zorder=2)

# Calculate means and standard deviations for each group
grouped_data = data.groupby('Study_Area')['Value']
means = grouped_data.mean()
stds = grouped_data.std()

# Define marker styles for each group
marker_styles = {'Hamilton Harbour': '*', 'WLO (Nearshore)': 'X', 'WLO (Offshore)': 'P'}

# Plot the means with different marker styles and format the legend label
for study_area, marker_style in marker_styles.items():
    mean_value = means[study_area]
    std_value = stds[study_area]
    x_position = list(data['Study_Area'].unique()).index(study_area) + 1  # Calculate the x position
    label = f'Mean (± SD) for {study_area} = {mean_value:.2f} (± {std_value:.2f})'
    ax.plot(x_position, mean_value, marker=marker_style, linewidth=0.25,  markersize=9, color='black', label=label, zorder=3) #edgecolors='black', s=100,

# Setting the x and y-axis labels
ax.set_xlabel('Measurement Location', fontsize=16, fontname='Times New Roman')
ax.set_ylabel('Chl-a Concentration (ug/L)', fontsize=16, fontname='Times New Roman')

# Customize tick parameters
plt.xticks(fontsize=14, fontname='Times New Roman')
plt.yticks(range(0, 51, 5), fontsize=14, fontname='Times New Roman') 

# Set the y-axis range with the buffer to include 0 to 50
ax.set_ylim([0, 50])

# Set y-axis to have ticks every 5 units from 0 to 50
ax.set_yticks(range(0, 51, 5))

# Plot the background shades for different concentration ranges
ax.axhspan(0, 0.9, color='lightgreen', alpha=0.35, lw=0.1, zorder=1)
ax.axhspan(0.9, 7.2, color='green', alpha=0.35, lw=0.1, zorder=1)
ax.axhspan(7.2, 55.5, color='darkgreen', alpha=0.35, lw=0.1, zorder=1)

plt.grid(False)
plt.suptitle('')
ax.set_title('')

# Create a custom legend handle for the outliers
outlier_handle = Line2D([0], [0], marker='o', color='black', linewidth=0.25, label='Outliers',
                        markerfacecolor='black', markersize=5)

# Create a FontProperties object to define the font properties
font_prop = FontProperties(family='Times New Roman', size=14)

# Retrieve the existing handles and labels
handles, labels = ax.get_legend_handles_labels()

# Add the custom handle to the handle list
handles.append(outlier_handle)

# Add the custom label to the label list
labels.append('Outliers')

# Create the new legend with the updated handles and labels and the font properties
ax.legend(handles=handles, labels=labels, prop=font_prop, framealpha=0.35)

# Tight layout for the plot
plt.tight_layout()
#plt.show()

# Save the figure in various formats
file_path_without_extension = "C:/Users/PHYS3009/Desktop/Matchup_Visualization/Matchup_Visualization"
fig.savefig(f'{file_path_without_extension}.svg', format='svg')

