# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 21:18:38 2020

@author: hgoer
"""

# Import libraries
import pandas as pd

from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool

# Read in data
df = pd.read_csv('https://raw.githubusercontent.com/hgoers/election_violence_dashboard/master/upcoming_election_vio.csv')[['date', 'status', 'country', 'pred_vio']]

# Filter for upcoming elections
df['date'] = pd.to_datetime(df['date'])

# Clean data
df['pred_vio'] = df['pred_vio']*100
df = df[df['date']>pd.to_datetime('today')].sort_values(by=['date']).head(10)
df = df.drop_duplicates(subset='country', keep='last').sort_values(by=['date'], ascending=False)
df = df.fillna(2)
df['date'] = df['date'].dt.strftime('%d-%m-%Y')

# Prepare data for visualisation
source = ColumnDataSource(df)
countries = source.data['country'].tolist()

vio = list(df['pred_vio'])

# Plot figure
p = figure(y_range=countries, x_range=(0,100), title='The predicted risk of election-related violence at upcoming elections', 
           x_axis_label='Predicted risk of election-related violence (%)',
           plot_width=1000,
           plot_height=600,
           tools='save')

p.hbar(y='country', right='pred_vio', height=0.5, color='orange', fill_alpha=0.5,
       source=source)

hover = HoverTool(tooltips = [('Election date', '@date'),
                              ('Election status', '@status'),
                              ('Risk of election violence (%)', '@pred_vio{1.11}')])
p.add_tools(hover)

p.yaxis.axis_label='Countries'
p.xgrid.grid_line_alpha=.75
p.ygrid.grid_line_alpha = .55

output_file('upcoming_elections.html')

curdoc().add_root(p)

#show(p)
