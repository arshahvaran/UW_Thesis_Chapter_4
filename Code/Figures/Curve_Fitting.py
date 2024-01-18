# -----------------------------Header information------------------------------
# Author: Ali Reza Shahvaran
# Filename: Curve_Fitting.py
# License: CC BY 4.0
# ----------------------------------------------------------------------------
# Description: This script is used for curve fitting and statistical analysis. It involves data manipulation, curve fitting using scipy, and calculation of various statistical metrics.
# ----------------------------------------------------------------------------
# Programming Language: Python 3.0
# Libraries: matplotlib, scipy, sklearn, pandas, numpy, math
# ----------------------------------------------------------------------------
# Input: Not specified in the initial part of the code.
# ----------------------------------------------------------------------------
# Output: Generates plots and statistical analysis results (details not specified in the initial part of the code).
# ----------------------------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error, mean_squared_log_error, mean_absolute_error, r2_score
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.model_selection import KFold
from math import exp, sqrt

# Set the global font to be Times New Roman
rcParams['font.family'] = 'Times New Roman'
rcParams['font.sans-serif'] = ['Times New Roman']

# Load data
file_path = "C:\\Users\\PHYS3009\\Desktop\\Matchup_Data_v4.xlsx"
data = pd.read_excel(file_path)
x_data = data['I3']
y_data = data['Log10_Value']

# Exponential fit function
def exp_func(x, a, b):
    return a * np.exp(b * x)

# Fit model for the entire dataset for plotting and R² calculation
params, covariance = curve_fit(exp_func, x_data, y_data)

# 5-fold cross-validation for first plot metrics
kf = KFold(n_splits=5)
rmsle_scores = []
mae_scores = []

for train_index, test_index in kf.split(x_data):
    x_train, x_test = x_data.iloc[train_index], x_data.iloc[test_index]
    y_train, y_test = y_data.iloc[train_index], y_data.iloc[test_index]

    # Fit model on training data
    params_cv, _ = curve_fit(exp_func, x_train, y_train)
    y_pred = exp_func(x_test, *params_cv)

    # Calculate metrics
    rmsle_scores.append(sqrt(mean_squared_log_error(y_test, y_pred)))
    mae_scores.append(mean_absolute_error(y_test, y_pred))

# Average metric scores for first plot
avg_rmsle = np.mean(rmsle_scores)
avg_mae = np.mean(mae_scores)

# R² for the entire dataset
y_pred_full = exp_func(x_data, *params)
r2 = r2_score(y_data, y_pred_full)

# Create a figure with two subplots
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(12, 6))

# First Plot: Original Data and Fitted Curve with Metrics
ax1.scatter(x_data, y_data, label='Data Points', color='dimgray', marker='X', s=14, edgecolor='k')
x_model = np.linspace(min(x_data), max(x_data), 1000)
y_model = exp_func(x_model, *params)
ax1.plot(x_model, y_model, color='dimgray', linestyle='-', label='Fitted Curve')
perr = np.sqrt(np.diag(covariance))
y_model_upper = exp_func(x_model, *(params + 1.96 * perr))
y_model_lower = exp_func(x_model, *(params - 1.96 * perr))
ax1.fill_between(x_model, y_model_lower, y_model_upper, color='gray', alpha=0.1, label='95% CI')
ax1.set_xlabel('I3', fontsize=14)
ax1.set_ylabel('Log(Chl-a)', fontsize=14)
ax1.legend(fontsize=14)
ax1.text(0.5, 0.985, '(b)', transform=ax1.transAxes, ha='center', va='top', fontsize=20)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)

# Display metrics for the first plot
textstr_1 = f'RMSLE: {avg_rmsle:.2f}\nR²: {r2:.2f}\nMAE: {avg_mae:.2f}'

ax1.text(0.655, 0.795, textstr_1, transform=ax1.transAxes, fontsize=14, verticalalignment='top')

# Second Plot: Actual vs. Modeled Plot with Logarithmic Scale
actual_values = 10 ** y_data
modeled_values = 10 ** exp_func(x_data, *params)
ax2.scatter(actual_values, modeled_values, label='Actual vs. Modeled', color='dimgray', marker='X', s=14, edgecolor='k')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.xaxis.set_major_formatter(ticker.LogFormatterMathtext())
ax2.yaxis.set_major_formatter(ticker.LogFormatterMathtext())
ax2.xaxis.set_major_locator(ticker.LogLocator(base=10.0))
ax2.yaxis.set_major_locator(ticker.LogLocator(base=10.0))
slope, intercept, _, _, _ = linregress(np.log10(actual_values), np.log10(modeled_values))
line = (10 ** intercept) * (actual_values ** slope)

# Calculate the residuals for the trend line in log scale
log_residuals = np.log10(modeled_values) - np.log10(line)

# Calculate the mean of the x-values
mean_x = np.mean(np.log10(actual_values))

# Calculate the sum of the squares of the differences between each x-value and the mean of x
sum_squares = np.sum((np.log10(actual_values) - mean_x) ** 2)

# Calculate the standard error of the regression
log_std_error = np.sqrt(np.sum(log_residuals ** 2) / (len(log_residuals) - 2))

# Generate a range of values for plotting the CI
x_range = np.linspace(min(actual_values), max(actual_values), 500)

# Calculate the trend line values for this range
line_range = (10 ** intercept) * (x_range ** slope)

# Calculate the 95% CI at each point
ci_range = 1.96 * log_std_error * np.sqrt(1/len(actual_values) + (np.log10(x_range) - mean_x)**2 / sum_squares)
log_upper_bound = np.log10(line_range) + ci_range
log_lower_bound = np.log10(line_range) - ci_range

# Transform the CI bounds back to linear scale
upper_bound = 10 ** log_upper_bound
lower_bound = 10 ** log_lower_bound

ax2.plot(actual_values, line, color='dimgray', linestyle='-', label='Trendline')
ax2.plot([min(actual_values), max(actual_values)], [min(actual_values), max(actual_values)], 'k--', label='Ideal Fit', linewidth=0.5)
ax2.fill_between(x_range, lower_bound, upper_bound, color='gray', alpha=0.1, label='95% CI')
ax2.set_xlabel('In-Situ Chl-a (μg/L)', fontsize=14)
ax2.set_ylabel('Modeled Chl-a (μg/L)', fontsize=14)
ax2.legend(fontsize=14)
ax2.text(0.5, 0.985, '(a)', transform=ax2.transAxes, ha='center', va='top', fontsize=20)
ax2.tick_params(axis='x', which = 'both', length=5, labelsize=14)
ax2.tick_params(axis='y', which = 'both', length=5, labelsize=14)

# Calculate RMSE, R², and MAE for Actual vs. Modeled
rmse_actual_modeled = sqrt(mean_squared_error(actual_values, modeled_values))
r2_actual_modeled = r2_score(actual_values, modeled_values)
mae_actual_modeled = mean_absolute_error(actual_values, modeled_values)

# Display metrics for the second plot
textstr_2 = f'RMSE: {rmse_actual_modeled:.2f}\nR²: {r2_actual_modeled:.2f}\nMAE: {mae_actual_modeled:.2f}'
ax2.text(0.020, 0.740, textstr_2, transform=ax2.transAxes, fontsize=14, verticalalignment='top')

# Add the mathematical expression of the fitted curve to the second plot
a, b = params
equation_text = f'y = {a:.2f}exp({b:.2f}x)'
ax1.text(0.345, 0.200, equation_text, transform=ax1.transAxes, fontsize=14, verticalalignment='top')

# Calculate slope and intercept for the trendline
slope, intercept, _, _, _ = linregress(np.log10(actual_values), np.log10(modeled_values))

# Add a text box to display slope and intercept
intercept_power_of_ten = 10 ** slope
trendline_text = f'Slope: {slope:.2f}\nIntercept: {intercept_power_of_ten:.2f}'
ax2.text(0.020, 0.620, trendline_text, transform=ax2.transAxes, fontsize=14, verticalalignment='top')

plt.tight_layout()
plt.savefig(r'C:\Users\PHYS3009\Desktop\Curve_Fitting\Curve_Fitting.svg', format='svg')
plt.show()
