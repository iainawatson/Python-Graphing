# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 14:15:45 2020

@author: iain
"""

# =============================================================================
# Create jitter plot of data
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
# \u00b5 = µ
x_label = ''
y_label = 'GFP puncta count\nin axons'
title = ''

# Enter names as list for renaming dataframe columns
cond_names = ['WT', 'A30P']

# =============================================================================
# Get .csv file
# =============================================================================
cwd = os.getcwd()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir = cwd, title = 'Choose csv to plot')
path = Path(file_path)
file = path.name
df = pd.read_csv(path)
groups = list(df)
n = len(groups)
# Repeat for creating hues for technical repeats on graph
root = tk.Tk()
root.withdraw()
file_path2 = filedialog.askopenfilename(initialdir = cwd, title = 'Choose csv with technical repeats list')
path2 = Path(file_path2)
df2 = pd.read_csv(path2)

# =============================================================================
# If a t-Test or similar has been run, the data frames need to be reduced to the 2 groups analysed
# =============================================================================
if os.path.exists('analysis_groups.pickle'):
    with open('analysis_groups.pickle', 'rb') as f:
        analysis_groups = pickle.load(f)
    df = df[analysis_groups]
    df2 = df2[analysis_groups]
    groups = list(df)
    n = len(groups)

# =============================================================================
# Rename dataframe titles
# =============================================================================
new_df = pd.DataFrame()
new_df2 = pd.DataFrame()
for i in range(n):
    new_name = cond_names[i]
    old_name = groups[i]
    new_df[new_name] = df[old_name]
    new_df2[new_name] = df2[old_name]

# =============================================================================
# Rearrange data into long format
# =============================================================================
list_groups = []
list_results = []
list_tech_rep = []
for i in cond_names:  
    for j in range(new_df.shape[0]):
        list_groups.append(i)
        list_results.append(new_df.loc[j, i])
        list_tech_rep.append(new_df2.loc[j, i])
newdf = pd.DataFrame({'group':list_groups, dep_var:list_results, 'tech_rep':list_tech_rep})
newdf_dropna = newdf.dropna() 

# =============================================================================
# Colour Palettes
# =============================================================================
pastel_cat_pal = sns.color_palette("Pastel1", n) #default categorical pastel

aruk_o_seq_pal = sns.light_palette('#dd5100', n, reverse = True) #sequential palette using ARUK orange, false is light to dark
aruk_b_seq_pal = sns.light_palette('#369ee0', n, reverse = True) #sequential palette using ARUK blue
aruk_p_seq_pal = sns.light_palette('#46163e', n, reverse = True) #sequential palette using ARUK purple

cool_div_pal = sns.color_palette("coolwarm", 7) # default divergent

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
sns.set(context = 'paper', font_scale = 1)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})

# Plot box plot: https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
meanlineprops = dict(linestyle = '--', linewidth = 1, color = line_colour)
ax = sns.boxplot(data = newdf_dropna, x = 'group', y = dep_var, width = 0.5, color = (1, 1, 1, 1), whis = 1.5, showmeans = True, meanline = True, meanprops = meanlineprops)

# Plot strip plot: https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
ax = sns.stripplot(data = newdf_dropna, x = 'group', y = dep_var, hue = 'tech_rep', jitter = True, edgecolor = line_colour, linewidth = 0.5, palette = "Pastel1", size = 3)

# Set the colour for all the boxes and lines on the boxplot
for i, artist in enumerate(ax.artists):
    artist.set_edgecolor(line_colour)
for j in range(len(ax.lines)):
    line = ax.lines[j]
    line.set_color(line_colour)
    line.set_mfc(line_colour)
    line.set_mec(line_colour)

# Set the title for the figure
ax.set_title(title, weight = 'bold')

# Set axis
ax.set_ylabel(y_label, weight = 'bold')
ax.set_xlabel(x_label, weight = 'bold')

# Control the legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels) # eg (handles=handles[1:0], labels=labels[1:0])
ax.legend(loc = 'best', frameon = True, fontsize = 8) # eg (loc = 'best', bbox_to_anchor=(0, 0),frameon = True)
ax.legend().remove()

# Edit the y labels, ideally just remove the highest and lowest
ax.yaxis.set_major_locator(MaxNLocator(prune='both', nbins = 'auto'))

# =============================================================================
# Save graph
# =============================================================================
name = file.strip('.csv')
fig = ax.get_figure()

graph_dir = cwd + '/graphs/'
if not os.path.exists(pathlib.Path(graph_dir)):
    os.makedirs(pathlib.Path(graph_dir))

fig.savefig(graph_dir + name + '_box_plot_with_jitter.pdf', bbox_inches='tight', dpi = 300, format = 'pdf')
