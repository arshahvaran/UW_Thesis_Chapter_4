# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: QA_Visualization.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script visualizes quality assurance data. It loads data from an Excel file, processes it to extract dates, and then uses matplotlib to create visual representations of this data.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, matplotlib, os
# ----------------------------------------------------------------------------
# Input: Reads from "QA_Results.xlsx" located at "C:\\Users\\PHYS3009\\Desktop\\L89_C2_L1_QA_Analysis".
# ----------------------------------------------------------------------------
# Output: Generates visual plots of the quality assurance data, saved to a specified directory.
# ----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

# Directory to save the figures
output_dir = "C:\\Users\\PHYS3009\\Desktop\\L89_C2_L1_QA_Analysis"

# Load the data from the "pixel_stats2" sheet
file_path = "C:\\Users\\PHYS3009\\Desktop\\L89_C2_L1_QA_Analysis\\QA_Results.xlsx"
df = pd.read_excel(file_path, sheet_name='pixel_stats2')

# Extracting dates from the "File_Name" column and creating a new "Date" column
df['Date'] = pd.to_datetime(df['File_Name'].str.extract('_(\d{8})_')[0])

# Sorting the DataFrame based on the "Date" column
df = df.sort_values(by='Date')

# Calculating the values for each specified group and creating new columns for them
df['High-Confidence Cloud/Cirrus'] = df[[22280, 55052, 54724]].sum(axis=1)
df['High-Confidence Cloud Shadow'] = df[23888]  
df['Cloud-Free Water'] = df[21952]
df['Cloud-Free Dry Land'] = df[21824]
df['Cloud-Free Snow/Ice'] = df[30048]
df['Low-Confidence Flags'] = 100 - df[['High-Confidence Cloud/Cirrus', 
                                       'High-Confidence Cloud Shadow', 
                                       'Cloud-Free Water', 
                                       'Cloud-Free Dry Land', 
                                       'Cloud-Free Snow/Ice']].sum(axis=1)


# Add this line before you define the create_plot function
df['Low-Confidence/No Cloud'] = 100 - df['High-Confidence Cloud/Cirrus']

# Function to create and save the plots
def create_plot(columns, title, file_name, colors):
    plt.figure(figsize=(12, 4))
    ax = df.set_index('Date')[columns].plot(kind='bar', stacked=True, figsize=(12, 4), color=colors, 
                                            edgecolor='black', linewidth=0.05, ax=plt.gca())
    plt.title(title)
    plt.xlabel('Year', fontsize=14, fontname='Times New Roman')
    plt.ylabel('Percentage (%)', fontsize=14, fontname='Times New Roman')
    
    # Setting x-axis ticks and labels to show only the first occurrence of each year
    years = df['Date'].dt.year
    labels = [str(year) if (year != years.iloc[i-1]) else '' for i, year in enumerate(years)]
    ax.set_xticklabels(labels, rotation=45)
    ax.set_ylim(0, 100)
    
    # Customizing the legend
    legend = ax.legend(loc='upper right', title=None, framealpha=0.75) 
    for text in legend.get_texts():
        text.set_fontsize(12)
        text.set_fontname('Times New Roman') 

    # Customizing tick labels
    for tick in ax.get_xticklabels():
        tick.set_fontsize(12)
        tick.set_fontname('Times New Roman')
    for tick in ax.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontname('Times New Roman')

    plt.tight_layout()

    # Save the figure in different formats with a DPI of 1200 for JPEG and EPS
    base_file_path = os.path.join(output_dir, file_name)
    plt.savefig(f'{base_file_path}.svg', format='svg') 

#plt.show()
#plt.close()

# Creating and saving the plots with specified colors and names
colors1 = ['black', 'dimgrey', 'deepskyblue', 'goldenrod', 'lightcyan', 'crimson']
create_plot(['High-Confidence Cloud/Cirrus', 'High-Confidence Cloud Shadow', 'Cloud-Free Water', 
             'Cloud-Free Dry Land', 'Cloud-Free Snow/Ice', 'Low-Confidence Flags'],
            '', 'full_plot', colors1)

colors2 = ['black', 'yellow']
create_plot(['High-Confidence Cloud/Cirrus', 'Low-Confidence/No Cloud'],
            '', 'cloud_plot', colors2)
