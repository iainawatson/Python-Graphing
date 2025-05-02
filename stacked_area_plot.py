# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:47:32 2019

@author: iain
"""

import os
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Variables
# =============================================================================
# Size of figure in inches
x_inches = 2
y_inches = 2

# =============================================================================
# Retrieve the csv file
# =============================================================================

#Enter .csv name below, copy from explorer
csv_name = 'transfection_efficiencies'

cwd = os.getcwd()
path = pathlib.Path(cwd + '/' + csv_name + '.csv')
df = pd.read_csv(path)

#to print the csv use below code
#print(df)
#can use the code below print the column titles
#print(list(df.columns))

# =============================================================================
# identify x and y data
# =============================================================================

#edit the column titles as necessary inorder to generate lists from the columns
list1 = df['GFP'].tolist()
list2 = df['α-Syn'].tolist()
list3 = df['A30P'].tolist()
list4 = df['A53T'].tolist()
ylist = [list1, list2, list3, list4]

#enter the necessary x values
xlist = ['1','2','4']
#xlist = [1,2,4]

# =============================================================================
# Colour Palettes
# =============================================================================
pastel_cat_pal = sns.color_palette("Pastel1") #default categorical pastel

aruk_o_seq_pal = sns.light_palette('#dd5100', reverse = True) #sequential palette using ARUK orange, false is light to dark
aruk_b_seq_pal = sns.light_palette('#369ee0', reverse = True) #sequential palette using ARUK blue
aruk_p_seq_pal = sns.light_palette('#46163e', reverse = True) #sequential palette using ARUK purple

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
fig = plt.figure(figsize = (x_inches,y_inches))
# control x and y limits
plt.ylim(0, 275)
plt.xlim(-0.1, 2.1)

# set seaborn parameters: https://seaborn.pydata.org/generated/seaborn.set.html
sns.set(context = 'paper', font_scale = 1)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})

# Set the font name for axis tick labels to be Comic Sans
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)

#plot the data (x, y, labels, colour)
plt.stackplot(xlist, ylist, labels = ['eGFP','WT','A30P','A53T'], colors = pastel_cat_pal)
plt.xlabel('DNA µg', fontsize = 10, weight = 'bold')
plt.ylabel('Transfection count', fontsize = 10, weight = 'bold') #weight can be normal
#plt.title('write title here', fontsize = 12, weight = 'bold')

# Control the legend
plt.legend(loc = 'best', frameon = True, fontsize = 8) # eg (loc = 'best', bbox_to_anchor=(0, 0),frameon = True)

# =============================================================================
# Save graph
# =============================================================================
save_path = pathlib.Path(cwd + '/' + csv_name + '.pdf')
fig.savefig(save_path, bbox_inches='tight', dpi = 300, format = 'pdf')
#plt.show()
