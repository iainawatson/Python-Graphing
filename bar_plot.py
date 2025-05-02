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

# =============================================================================
# Variables
# =============================================================================
#enter the dependent variable for the analysis, eg area, count...
dep_var = 'area'

# Size of figure in inches
x_inches = 3
y_inches = 2.5

# Enter names for graph x and y labels. Uncomment lines as necessary below in Plot data section
# \u00b2 = ^2 symbol
# \u00b2 = ^3 symbol
x_label = 'Transfection'
y_label = 'Mean bouton area (µm\u00b2)'
title = 'Effect of transfections of bouton area size'

# Enter names as list for renaming dataframe columns
cond_names = ['eGFP', 'WT', 'A30P']

# Comment out for error to show SEM or SD
#error = 'SD'
error = 'SEM'

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
file2 = path2.name
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
if error == 'SD':
    value = 'sd'
else:
    value = 68
line_colour = '0.5'
plt.figure(figsize=(x_inches,y_inches))
# set seaborn parameters: https://seaborn.pydata.org/generated/seaborn.set.html
sns.set(style = 'whitegrid', context = 'paper', palette = "Pastel1", font_scale = 1)
# Plot bar chart: https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot
ax = sns.barplot(data = newdf_dropna, x = 'group', y = dep_var, ci = value, facecolor = (1, 1, 1, 1), errcolor = line_colour, edgecolor = line_colour, capsize = .2, errwidth = 1, linewidth = 1)
# Plot strip plot: https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
ax = sns.stripplot(data = newdf_dropna, x = 'group', y = dep_var, hue = 'tech_rep', jitter = True, linewidth = 0.5, edgecolor = line_colour, size = 3)
# Set axis: 
ax.set_ylabel(y_label, weight = 'bold')
ax.set_xlabel(xlabel = '')
#ax.set_title(title, weight = 'bold')
ax.legend().remove()

# =============================================================================
# Save graph
# =============================================================================
name = file.strip('.csv')
fig = ax.get_figure()

graph_dir = cwd + '/graphs/'
if not os.path.exists(pathlib.Path(graph_dir)):
    os.makedirs(pathlib.Path(graph_dir))

fig.savefig(graph_dir + name + '_bar_chart_' + error + '.pdf', bbox_inches='tight', dpi = 300, format = 'pdf')