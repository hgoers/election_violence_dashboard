#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:17:15 2020

@author: hgoers
"""

# Import libraries
import pandas as pd
import numpy as np

import geopandas as gpd
import json

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column

# Read in electoral violence data data
df = pd.read_csv('https://raw.githubusercontent.com/OEFDataScience/REIGN_Dashboard/dd4b14f8172651a720f686b0f1bfbc3cc3a777c3/elvis_master_sept2019_final.csv')
df = df.set_index('Unnamed: 0')

# Read in with REIGN data, merge with df
reign = pd.read_csv('https://raw.githubusercontent.com/OEFDataScience/REIGN.github.io/gh-pages/data_sets/REIGN_2020_9.csv')[['country', 'leader', 'year', 'month', 'tenure_months', 'government', 'anticipation']]
df = pd.merge(reign, df, on=['country', 'year', 'month'], how='left')

# Filter data for current year
df = df[df['year']==2018]

# Fill missing election dates with 'no election'
df['dates'].fillna('No election', inplace=True)

# Split data into election and no election
df_elections = df[df['dates']!='No election'].drop_duplicates()
df_no_elections = df[df['dates']=='No election'].drop_duplicates()
df_no_elections = df_no_elections[df_no_elections['month']==9]

# Create dummy risk value
df_elections['pred_risk'] = (df_elections['tenure_months'] / df_elections['tenure_months']) * np.random.uniform(size=df_elections.shape[0])

# Join again
df_joined = df_elections.append(df_no_elections, ignore_index=True)
df_joined = df_joined.drop_duplicates(subset='country', keep='first')

# Read in map data
gdf = gpd.read_file('https://raw.githubusercontent.com/hgoers/hgoers.github.io/master/worldmap.json')[['admin', 'adm0_a3', 'geometry']]
gdf = gdf.replace('United States of America', 'USA')
gdf = gdf.set_geometry('geometry')
gdf.columns = ['country', 'stateabb', 'geometry']

# Merge df with gdf
merged = pd.merge(gdf, df_joined, on='country', how='left')

# Read data to json
merged_json = json.loads(merged.to_json())

# Convert to String like object
json_data = json.dumps(merged_json)

# Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson = json_data)

# Define a sequential multi-hue color palette
palette = brewer['YlGnBu'][5]

# Reverse colour order so that dark blue is highest risk
palette = palette[::-1]

# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 1, 
                                 nan_color = '#d9d9d9')

# Define custom tick labels for color bar
tick_labels = {'0':'Low risk',
               '0.2':'',
               '0.4':'',
               '0.6':'',
               '0.8':'',
               '1':'High risk'}

# Create colour bar 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff = 12, 
                     border_line_color = None, location = (0,0), major_label_overrides = tick_labels)

# Create figure object
p = figure(title = 'Risk of election violence over the next six months', plot_height = 500, 
           plot_width = 1000, toolbar_location = 'above', tools = 'save')
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.axis.visible = False

# Add patch renderer to figure 
p.patches('xs', 'ys', source = geosource, fill_color = {'field' :'pred_risk', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

# Add hover tool
hover = HoverTool(tooltips = [('Country','@country'),
                              ('Current leader', '@leader'),
                              ('Leader tenure (months)', '@tenure_months'),
                              ('Regime type', '@government'),
                              ('Election date', '@dates'),
                              ('Risk of election violence', '@pred_risk')])

p.add_tools(hover)

# Specify figure layout
p.add_layout(color_bar, 'right')

# Display figure
show(p)
