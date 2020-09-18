#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:17:15 2020
@author: hgoers
"""

# Import libraries
import pandas as pd

from clean_names import *

import geopandas as gpd
import json

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import HoverTool

# Read in upcoming elections vio data
df = pd.read_csv('https://raw.githubusercontent.com/hgoers/election_violence_dashboard/master/upcoming_election_vio.csv')[['country', 'date', 'status', 'pred_vio']]

df['date'] = pd.to_datetime(df['date']) 
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Shift dates to string to accommodate json
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Read in REIGN data
reign = pd.read_csv('https://raw.githubusercontent.com/OEFDataScience/REIGN.github.io/gh-pages/data_sets/REIGN_2020_9.csv')[['country', 'leader', 'year', 'month', 'tenure_months', 'government', 'anticipation']]
reign = reign[reign['year']>2019]

# Read in map data
gdf = gpd.read_file('https://raw.githubusercontent.com/hgoers/hgoers.github.io/master/worldmap.json')[['admin', 'geometry']]
gdf = gdf.set_geometry('geometry')
gdf.columns = ['country', 'geometry']

# Clean country names
reign['country'] = clean_names(reign['country'])
gdf['country'] = clean_names(gdf['country'])

# Create elections data
elections_df = pd.merge(df, reign, on=['country', 'month', 'year'], how='outer')

# Fill missing election dates with 'no election'
elections_df['date'].fillna('No upcoming election', inplace=True)

# Merge df with gdf
merged = pd.merge(gdf, elections_df, on='country', how='left')

# Keep only latest information
merged = merged.sort_values(by=['year', 'month', 'date'], ascending=False).drop_duplicates(subset='country')

# Get current leaders
current_leaders = reign.sort_values(by=['year', 'month'], ascending=False).drop_duplicates(subset='country')[['country', 'leader']]

# Complete dataset
merged = pd.merge(merged, current_leaders, on='country', how='left')
merged['pred_vio'] = merged['pred_vio']*100

# Read data to json
merged_json = json.loads(merged.to_json())

# Convert to string like object
json_data = json.dumps(merged_json)

# Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson = json_data)

# Define a sequential multi-hue color palette
palette = brewer['YlGnBu'][5]

# Reverse colour order so that dark blue is highest risk
palette = palette[::-1]

# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 100, 
                                 nan_color = '#d9d9d9')

# Define custom tick labels for color bar
tick_labels = {'0':'Low risk',
               '20':'',
               '40':'',
               '60':'',
               '80':'',
               '100':'High risk'}

# Create colour bar 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff = 12, 
                     border_line_color = None, location = (0,0), major_label_overrides = tick_labels)

# Create figure object
p = figure(title = ('Risk of election violence for upcoming elections up to ' + str(int(merged['year'].max()))), 
           plot_height = 500, plot_width = 1000, toolbar_location = 'above', tools = 'save')
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.axis.visible = False

# Add patch renderer to figure 
p.patches('xs', 'ys', source = geosource, fill_color = {'field':'pred_vio', 'transform':color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

# Add hover tool
hover = HoverTool(tooltips = [('Country','@country'),
                              ('Current leader', '@leader_y'),
                              ('Election date', '@date'),
                              ('Risk of election violence (%)', '@pred_vio{1.11}')])

p.add_tools(hover)

# Specify figure layout
p.add_layout(color_bar, 'right')

curdoc().add_root(p)

# Display figure, comment out for heroku deployment
#show(p)
