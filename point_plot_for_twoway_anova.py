# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 01:48:14 2020

@author: iain
"""

# =============================================================================
# Create a point plot to asses data distribution
# =============================================================================

import os
import pandas as pd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# =============================================================================
# Variables
# =============================================================================
#enter the dependent variable for the analysis, eg area, count...
dep_var = 'area'

# Size of figure in inches
x_inches = 1.4
y_inches = 2

# Enter names for graph x and y labels. Uncomment lines as necessary below in Plot data section
# \u00b2 = ^2 symbol
# \u00b2 = ^3 symbol
# \u00b5 = µ
x_label = ''
y_label = 'GFP puncta area (\u00b5m\u00b2)'
#title = 'Effect of transfections of bouton area size'

# Comment out for error to show SEM or SD
error = 'SD'
# error = 'SEM'

# =============================================================================
# Get the long formatted data
# =============================================================================
file_list = os.listdir()
for i in file_list:
    if i.endswith('_combined_data.csv'):
        file = i
    elif i.endswith('_outliers_removed.csv'):
        file = i
df = pd.read_csv(file)

# =============================================================================
# Set the font
# =============================================================================
# Changes the default font. Then, "ALWAYS use sans-serif fonts"
plt.rcParams['font.sans-serif'] = "CMU Sans Serif"
plt.rcParams['font.family'] = "sans-serif"

# =============================================================================
# Plot data
# =============================================================================
# Select the correct error bars
if error == 'SD':
    value = 'sd'
else:
    value = 68

# Set the figure parameters
plt.figure(figsize=(x_inches,y_inches))
# control x and y limits, remove for logs
# plt.ylim(0, None)
# plt.xlim(0, None)

line_colour = '0.5'
# set seaborn parameters: https://seaborn.pydata.org/generated/seaborn.set.html
sns.set(context = 'paper', font_scale = 1)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})

# Draw the graph
ax = sns.pointplot(x='subgroup', y=dep_var, hue='group', data=df, dodge = True, palette = 'Pastel1', ci = value, errwidth = 1, capsize=.2)

# Set the title for the figure
#ax.set_title(title, weight = 'bold')

# Set axis
ax.set_ylabel(y_label, weight = 'bold')
ax.set_xlabel(x_label, weight = 'bold')

# Control the legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels) # eg (handles=handles[1:0], labels=labels[1:0])
ax.legend(loc = 'upper right', frameon = True, fontsize = 8) # eg (loc = 'best', bbox_to_anchor=(0, 0),frameon = True)
# ax.legend().remove()

# Edit the y labels, ideally just remove the highest and lowest
ax.yaxis.set_major_locator(MaxNLocator(prune='upper', nbins = 'auto'))

# Set the y scale if necessary
ax.set_yscale('log') # value = {"linear", "log", "symlog", "logit", ...}, basey = 10, 2 etc...

# =============================================================================
# Save graph
# =============================================================================
name = file.strip('.csv')
fig = ax.get_figure()

cwd = os.getcwd()
graph_dir = cwd + '/graphs/'
if not os.path.exists(pathlib.Path(graph_dir)):
    os.makedirs(pathlib.Path(graph_dir))

fig.savefig(graph_dir + name + '_point_plot_for_twoway_'+error+'_bars.pdf', bbox_inches='tight', dpi = 300, format = 'pdf')
