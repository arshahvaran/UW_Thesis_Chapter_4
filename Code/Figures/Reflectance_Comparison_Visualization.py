# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Reflectance_Comparison_Visualization.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script visualizes reflectance comparison data. It loads merged data from an Excel file, processes it, and creates visualizations comparing different types of reflectance at various wavelengths.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, matplotlib, numpy
# ----------------------------------------------------------------------------
# Input: Reads from "Merged.xlsx" located at "C:\\Users\\PHYS3009\\Desktop\\Merge".
# ----------------------------------------------------------------------------
# Output: Produces visual plots comparing reflectance.
# ----------------------------------------------------------------------------


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

# Load the data
file_path = "C:\\Users\\PHYS3009\\Desktop\\Merge\\Merged.xlsx"
data = pd.read_excel(file_path)

# Extract wavelengths and their respective column names for rhow and rhot
wavelengths = [443, 483, 561, 655, 865]
rhow_columns = [f'rhow_{w}' for w in wavelengths]
rhot_columns = [f'rhot_{w}' for w in wavelengths]

# Adjust Value_x for brightness to start from the middle of the color palette
data['Value_x_adjusted'] = 0.55 + (data['Value_x'] - data['Value_x'].min()) / (2 * (data['Value_x'].max() - data['Value_x'].min()))

# Set the figure size to have a 2:1 aspect ratio
fig, ax = plt.subplots(figsize=(10, 5))

# Define the x-axis and y-axis limits
xmin, xmax = 443, 865
ymin, ymax = data[rhow_columns + rhot_columns].min().min(), data[rhow_columns + rhot_columns].max().max()
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Create a continuous spectrum background using 'nipy_spectral'
# Generate an image array, with colors along the second dimension (axis=1)
spectrum_image = np.linspace(0, 0.01, 5000)
spectrum_image = np.tile(spectrum_image, (10, 1))

# Display the spectrum image with the 'nipy_spectral' colormap
ax.imshow(spectrum_image, aspect='auto', extent=[415, 670, ymin, ymax], cmap='nipy_spectral', origin='lower', alpha=0.25)

# Fill the background after the spectrum with color #eaeaea
ax.axvspan(670, xmax, color='#f2f2f2', zorder=0)


# Define a function to plot the lines with a fixed alpha for transparency
def plot_line(group_columns, cmap, alpha=1):
    for index, row in data.iterrows():
        y_values = row[group_columns].values
        brightness = row['Value_x_adjusted']
        ax.plot(wavelengths, y_values, color=cmap(brightness), alpha=alpha)

# Create the colormaps
cyan_cmap = plt.get_cmap('Blues')
purple_cmap = plt.get_cmap('Oranges')

# Sort the DataFrame by 'Value_x_adjusted' for rhot plotting
sorted_data_rhot = data.sort_values(by='Value_x_adjusted')


# Normalize 'Value_x' for line thickness between a minimum and maximum line width
min_line_width = 0.75  # Set minimum line width
max_line_width = 1.5  # Set maximum line width
line_widths = min_line_width + (data['Value_x'] - data['Value_x'].min()) / (data['Value_x'].max() - data['Value_x'].min()) * (max_line_width - min_line_width)

linestyle = '--'
# '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
# Plot the rhot lines first
for index, row in sorted_data_rhot.iterrows():
    y_values = row[rhot_columns].values
    brightness = row['Value_x_adjusted']
    line_width = line_widths.iloc[index]
    ax.plot(wavelengths, y_values, color=purple_cmap(brightness), alpha=1, linewidth=line_width, linestyle=linestyle)

# Sort the DataFrame by 'Value_x_adjusted' for rhow plotting
sorted_data_rhow = data.sort_values(by='Value_x_adjusted')

# Plot the rhow lines on top of rhot lines
for index, row in sorted_data_rhow.iterrows():
    y_values = row[rhow_columns].values
    brightness = row['Value_x_adjusted']
    line_width = line_widths.iloc[index]
    ax.plot(wavelengths, y_values, color=cyan_cmap(brightness), alpha=1, linewidth=line_width, linestyle=linestyle)



# Set the font for the ticks and labels
font_name = 'Times New Roman'
font_size = 12

# Set the custom x-axis ticks and labels
ax.set_xticks([443, 483, 561, 655, 865])
ax.set_xticklabels(['443', '483', '561', '655', '865'], fontname=font_name, fontsize=font_size)

# Set the font for the ticks
ax.tick_params(axis='both', labelsize=font_size, labelcolor='black')

# Set the font for the y-axis tick labels
for label in ax.get_yticklabels():
    label.set_fontname(font_name)
    label.set_fontsize(font_size)
    
# Label the axes
ax.set_xlabel('Wavelength (nm)', fontname=font_name, fontsize=font_size+2)
ax.set_ylabel('Reflectance', fontname=font_name, fontsize=font_size+2)

# Make the plot layout tight
plt.tight_layout()





# Create custom lines for the legend
orange_line = mlines.Line2D([], [], color='darkorange', markersize=15, label=r'TOA Reflectance ($\rho_t$)', linestyle='--')
blue_line = mlines.Line2D([], [], color='blue', markersize=15, label=r'Water-Leaving Reflectance ($\rho_w$)', linestyle='--')

# Define font properties for the legend
legend_font_props = {'family': font_name, 'size': font_size}

# Add the legend to the plot with the custom font properties
ax.legend(handles=[orange_line, blue_line], loc='upper right', prop=legend_font_props)


# Define the base file path without extension
file_path_without_extension = "C:\\Users\\PHYS3009\\Desktop\\Merge\\Visualization1"

# Save the figure in various formats
fig.savefig(f'{file_path_without_extension}.svg', format='svg', dpi=1200)
#fig.savefig(f'{file_path_without_extension}.png', format='png', dpi=1200)
#fig.savefig(f'{file_path_without_extension}.eps', format='eps', dpi=1200)

# Show the plot
#plt.show()
