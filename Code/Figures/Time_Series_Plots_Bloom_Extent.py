# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Time_Series_Plots_Bloom_Extent.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script generates time series plots to visualize the extent of blooms. It includes data loading, processing, and visualization using matplotlib with various customizations.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, matplotlib, datetime, numpy
# ----------------------------------------------------------------------------
# Input: The specific input file is not indicated in the initial part of the code.
# ----------------------------------------------------------------------------
# Output: Produces time series plots visualizing bloom extent.
# ----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.patches import Patch
from matplotlib import rcParams
import matplotlib.ticker as ticker
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.legend_handler as lh
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

# Set the global font to be Times New Roman
rcParams['font.family'] = 'Times New Roman'
rcParams['font.sans-serif'] = ['Times New Roman']


#Create a color map instance for 'Greys'
cmap = plt.cm.Greys
norm = Normalize(vmin=0, vmax=100)

#Create a ScalarMappable and initialize a colorbar
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])


# Create proxy artists for the legend
legend_elements = [Patch(facecolor='k', label='Max'),
                   Patch(facecolor='dimgrey', label='Avg')]

# Original file path
#excel_file_path = "C:\\Users\\PHYS3009\\Desktop\\Time_Series_Plots\\Chla_Outputs_HH.xlsx"
#excel_file_path = "C:\\Users\\PHYS3009\\Desktop\\Time_Series_Plots\\Chla_Outputs_WLON.xlsx"
excel_file_path = "C:\\Users\\PHYS3009\\Desktop\\Time_Series_Plots\\Chla_Outputs_WLOO.xlsx"

# Load the data
df = pd.read_excel(excel_file_path)

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter out rows where 'Data_Availibity_%' is zero
df = df[df['Data_Availibity_%'] != 0]
df2 = df[df['Bloom_Extent_km2'] != 0]

# Sort the DataFrame by the 'Date' column
df2 = df2.sort_values(by='Date')

# Figure setup
fig = plt.figure(figsize=(15, 3))  

# Adjust subplot sizes
gs = fig.add_gridspec(1, 5) 

# Plot 1 - Scatter plot with dates (taking up 3 columns of the grid)
ax1 = fig.add_subplot(gs[0, 0:3])

# Adding the grey bars with varying intensity based on 'Data_Availabilty_%'
for idx, row in df2.iterrows():
    # Normalize the data availability to a range between 0 and 1
    grey_intensity = 1 - (row['Data_Availibity_%'] / 100.0)
    # Create a grey color with the calculated intensity and 50% transparency
    color = (grey_intensity, grey_intensity, grey_intensity, 0.3)
    ax1.axvline(x=row['Date'], color=color, zorder=1)

ax1.plot(df2['Date'], df2['Bloom_Extent_km2'], label='Bloom Extent', marker='o', markerfacecolor='none', markeredgecolor='k', markersize=4.5 , linestyle='--', color='k', linewidth=0.6, zorder=2)
ax1.set_xlim([datetime(2013, 1, 1), datetime(2023, 12, 31)])
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax1.set_xlabel('Year', fontsize=12, fontname='Times New Roman')
ax1.set_ylabel('Bloom Extent (km²)', fontsize=12, fontname='Times New Roman')
ax1.tick_params(axis='both', which='major', labelsize=10)
#ax1.set_ylim([9, 25])
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.3f}'.format(x)))
#ax1.legend(handles=legend_elements2, loc='upper right')

shiftvalue = 0.3975
shiftvalue2 = -0.010

# Define the rectangle with rounded edges
rounded_rect = FancyBboxPatch(((0.0475+shiftvalue), (0.775+shiftvalue2)), 0.145, 0.135, linewidth=1, edgecolor='dimgrey', facecolor='white', alpha=0.5, boxstyle="round,pad=0.005", transform=fig.transFigure)
#Add the rounded rectangle to the figure
fig.patches.append(rounded_rect)

# Create a new axes for the colorbar
cbar_ax = fig.add_axes([(0.05+shiftvalue), (0.85+shiftvalue2), 0.05, 0.036]) 

# Add the colorbar to the plot
cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.ax.set_xticklabels(['0', '100'])  # Set the text for the ticks
fig.text((0.11+shiftvalue), (0.849+shiftvalue2), 'Data Availability %', fontsize=10, fontname='Times New Roman')

#fig.text(0.065, 0.849 + shiftvalue2, 'Hamilton Harbour', fontsize=14, fontname='Times New Roman', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))
#fig.text(0.065, 0.849 + shiftvalue2, 'Western Lake Ontario: Nearshore', fontsize=14, fontname='Times New Roman', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))
fig.text(0.065, 0.849 + shiftvalue2, 'Western Lake Ontario: Offshore', fontsize=14, fontname='Times New Roman', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))

# Plot 2 - Bar plot of average intensity per year (taking up 1 column of the grid)
ax2 = fig.add_subplot(gs[0, 3])
yearly_avg = df.groupby('Year')['Bloom_Extent_km2'].mean()
yearly_max = df.groupby('Year')['Bloom_Extent_km2'].max()
ax2.bar(yearly_max.index, yearly_max.values, color='k')
ax2.bar(yearly_avg.index, yearly_avg.values, color='dimgrey')
ax2.set_xlabel('Year', fontsize=12, fontname='Times New Roman')
#ax2.set_ylabel('Average Bloom Intensity (ug/L)', fontsize=12, fontname='Times New Roman')
ax2.tick_params(axis='x', labelsize=10, rotation=45)
ax2.tick_params(axis='y', labelsize=10)
ax2.set_xticks(yearly_avg.index)
#ax2.set_ylim([0, 25])
ax2.legend(handles=legend_elements, loc='upper right')

#Ensure all year labels are displayed
ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Set x-ticks for each year
ax2.set_xticks(range(2013, 2024))

# Set x-tick labels for each year
ax2.set_xticklabels(range(2013, 2024))

# Plot 3 - Bar plot of average intensity per month (taking up 1 column of the grid)
ax3 = fig.add_subplot(gs[0, 4])

# Ensuring all months are represented
monthly_avg = df.groupby('Month')['Bloom_Extent_km2'].mean().reindex(range(1, 13), fill_value=0)
monthly_max = df.groupby('Month')['Bloom_Extent_km2'].max().reindex(range(1, 13), fill_value=0)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax3.bar(months, monthly_max.values, color='k')
ax3.bar(months, monthly_avg.values, color='dimgrey')
ax3.set_xlabel('Month', fontsize=12, fontname='Times New Roman')
#ax3.set_ylabel('Average Bloom Intensity (ug/L)', fontsize=12, fontname='Times New Roman')
#ax3.tick_params(axis='both', which='major', labelsize=10, rotation=45)
ax3.tick_params(axis='x', labelsize=10, rotation=45)
ax3.tick_params(axis='y', labelsize=10)

#ax3.set_ylim([0, 25])
ax3.legend(handles=legend_elements, loc='upper right')

#Layout adjustments
plt.tight_layout()

# Change the extension from .xlsx to .svg
output_file_path = excel_file_path.rsplit('.', 1)[0] + '.svg'

# Save the figure
fig.savefig(output_file_path)

#Display the plots
plt.show()