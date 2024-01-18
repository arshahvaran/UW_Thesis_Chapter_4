# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: SHAP_Value.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script uses the SHAP (SHapley Additive exPlanations) library to analyze the impact of features in a dataset on a model's predictions. It includes data loading, processing, model training with a random forest regressor, and SHAP value calculation and visualization.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: pandas, shap, sklearn, matplotlib
# ----------------------------------------------------------------------------
# Input: Reads data from "Matchup_Data_v4.xlsx" located at "C:\\Users\\PHYS3009\\Desktop\\Chapter3".
# ----------------------------------------------------------------------------
# Output: Visualizes the SHAP values to interpret the model's predictions.
# ----------------------------------------------------------------------------

import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import matplotlib as mpl

# Load data from the Excel file
file_path = "C:\\Users\\PHYS3009\\Desktop\\Chapter3\\Matchup_Data_v4.xlsx"
data = pd.read_excel(file_path)

# Separate the independent and dependent variables
X = data[["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]]
y = data["Log10_Value"]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(random_state=0)
model.fit(X_train, y_train)

# Calculate SHAP values
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)

# Set the font details for the plot
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12

# Create a figure with a specific size
plt.figure(figsize=(10/1.25, 8/1.25))

# Create a bar plot
shap.plots.bar(shap_values, show=False)

# Customizing the plot
plt.gca().set_xlabel('Mean(|SHAP Value|)', fontsize=11, fontname='Times New Roman')

# Changing the color of the bars
for bar in plt.gca().patches:
    bar.set_facecolor('#e22566')

# Adjusting font size of y-axis labels and the numbers after each bar
plt.gca().tick_params(axis='y', labelsize=12, colors='black') # Change y-axis label colors to black
plt.gca().tick_params(axis='x', labelsize=12)

# Adjust layout
plt.tight_layout()

# Save the figure as an SVG file
plt.savefig("C:\\Users\\PHYS3009\\Desktop\\Chapter3\\SHAP_Value\\SHAP_Value.svg", format='svg', bbox_inches='tight')

plt.show()
