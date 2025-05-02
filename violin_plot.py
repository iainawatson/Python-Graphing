# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 13:31:57 2020

@author: iain
"""

# =============================================================================
# Create violin plot of data
# =============================================================================

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt

# =============================================================================
# Variables
# =============================================================================
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

# =============================================================================
# Get .csv file
# =============================================================================
cwd = os.getcwd()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir = cwd, title = 'Choose csv to plot')
path = pathlib.Path(file_path)
file = path.name
df = pd.read_csv(file)
groups = list(df)
n = len(groups)

# =============================================================================
# Rename dataframe titles
# =============================================================================
new_df = pd.DataFrame()
for i in range(len(groups)):
    new_name = cond_names[i]
    old_name = groups[i]
    new_df[new_name] = df[old_name]

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
plt.figure(figsize=(x_inches,y_inches))
# set seaborn parameters: https://seaborn.pydata.org/generated/seaborn.set.html
sns.set(style = 'whitegrid', context = 'paper', palette = "Pastel1", font_scale = 1)
# Plot violin plot: https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot
ax = sns.violinplot (data = new_df, inner = 'quartile')
# Set axis: 
ax.set_ylabel(y_label, weight = 'bold')
#ax.set_xlabel(xlabel = None)
#ax.set_title(title, weight = 'bold')

# =============================================================================
# Save graph
# =============================================================================
name = file.strip('.csv')
fig = ax.get_figure()

graph_dir = cwd + '/graphs/'
if not os.path.exists(pathlib.Path(graph_dir)):
    os.makedirs(pathlib.Path(graph_dir))

fig.savefig(graph_dir + name + '_violin_plot.pdf', bbox_inches='tight', dpi = 300, format = 'pdf')
