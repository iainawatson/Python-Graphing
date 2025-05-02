# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# =============================================================================
# Create a point plot to asses data distribution
# =============================================================================

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pathlib
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from matplotlib.ticker import MaxNLocator

# =============================================================================
# Variables
# =============================================================================
#enter the dependent variable for the analysis, eg area, count...
dep_var = 'count'

# Size of figure in inches
x_inches = 2
y_inches = 2

# Enter names for graph x and y labels. Uncomment lines as necessary below in Plot data section
# \u00b2 = ^2 symbol
# \u00b2 = ^3 symbol
# x_label = ''
y_label = 'Mean GFP puncta count'
#title = 'Effect of transfections of bouton area size'

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
# Set the figure parameters
plt.figure(figsize=(x_inches,y_inches))
# control x and y limits
plt.ylim(0, 4)
plt.xlim(0, None)

line_colour = '0.5'
# set seaborn parameters: https://seaborn.pydata.org/generated/seaborn.set.html
sns.set(style = 'whitegrid', context = 'paper', font_scale = 1)

# Draw the graph. help at: https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
meanlineprops = dict(linestyle = '--', linewidth = 1, color = line_colour)
ax = sns.boxplot(data = df, x = 'subgroup', y = dep_var, hue = 'group', width = 0.5, palette = "Pastel1", whis = 1.5, showmeans = True, meanline = True, meanprops = meanlineprops)

# Set the colour for all the boxes and lines on the boxplot
for i, artist in enumerate(ax.artists):
    artist.set_edgecolor(line_colour)
for j in range(len(ax.lines)):
    line = ax.lines[j]
    line.set_color(line_colour)
    line.set_mfc(line_colour)
    line.set_mec(line_colour)
    
# Set the title for the figure
#ax.set_title(title, weight = 'bold')

# Set axis
ax.set_ylabel(y_label, weight = 'bold')
ax.set_xlabel(xlabel = '')

# Control the legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels) # eg (handles=handles[1:0], labels=labels[1:0])
ax.legend(loc = 'lower left', frameon = True, fontsize = 8) # eg (loc = 'best', bbox_to_anchor=(0, 0),frameon = True)
# ax.legend().remove()

# Edit the y labels, ideally just remove the highest and lowest
ax.yaxis.set_major_locator(MaxNLocator(prune='both', nbins = 'auto'))

# =============================================================================
# Save graph
# =============================================================================
name = file.strip('.csv')
fig = ax.get_figure()

cwd = os.getcwd()
graph_dir = cwd + '/graphs/'
if not os.path.exists(pathlib.Path(graph_dir)):
    os.makedirs(pathlib.Path(graph_dir))

fig.savefig(graph_dir + name + '_boxplot_for_twoway.pdf', bbox_inches='tight', dpi = 300, format = 'pdf')


