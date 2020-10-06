#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:17:15 2020

@author: hgoers
"""

# Import libraries
import pandas as pd

from datetime import datetime

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
reign = pd.read_csv('https://raw.githubusercontent.com/OEFDataScience/REIGN.github.io/gh-pages/data_sets/REIGN_2020_10.csv')[['country', 'leader', 'year', 'month', 'tenure_months', 'government', 'anticipation']]
df = pd.merge(reign, df, on=['country', 'year', 'month'], how='left')
df = df[df['year']==2018]

# Fill missing election dates with 'no election'
df['dates'].fillna('No election', inplace=True)

# Read in map data
gdf = gpd.read_file('https://raw.githubusercontent.com/hgoers/hgoers.github.io/master/worldmap.json')[['admin', 'adm0_a3', 'geometry']]
gdf = gdf.set_geometry('geometry')
gdf.columns = ['country', 'stateabb', 'geometry']

# Get current month
datem = datetime.now().month

# Create a function the returns json_data for the month selected by the user
def json_data(selectedMonth):    
    mth = selectedMonth

    # Pull selected month from data
    df_mth = df[df['month'] == mth]
    
    # Merge the GeoDataframe object (gdf) with the data (df)
    merged = pd.merge(gdf, df_mth, on='country', how='left')
        
    # Convert to json
    merged_json = json.loads(merged.to_json())
    
    # Convert to json preferred string-like object 
    json_data = json.dumps(merged_json)
    return json_data

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # The input mth is the month selected from the slider
    mth = slider.value + datem
    new_data = json_data(mth)
    
    # Update the plot based on the changed inputs
    p = make_plot(input_field)
    
    # Update the layout, clear the old document and display the new document
    layout = column(p, widgetbox(slider))
    curdoc().clear()
    curdoc().add_root(layout)
    
    # Update the data
    geosource.geojson = new_data

# Create a plotting function
def make_plot(field_name):
    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = df['logpredict'].max(), nan_color = '#d9d9d9')

    # Create colour bar
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff = 12, width = 20, 
                         border_line_color = None, location = (0,0))

    # Create figure object
    p = figure(title = 'Forecasted risk of election violence', plot_height = 500, 
               plot_width = 1000, toolbar_location = 'above', tools = 'save')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    
    # Add patch renderer to figure
    p.patches('xs','ys', source = geosource, fill_color = {'field':'logpredict', 'transform':color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    
    # Specify color bar layout
    p.add_layout(color_bar, 'right')
    
    # Add the hover tool to the graph
    p.add_tools(hover)
    
    return p

# Input geojson source that contains features for plotting for:
# Current month
geosource = GeoJSONDataSource(geojson = json_data(datem))
input_field = 'logpredict'

# Define a sequential multi-hue color palette
palette = brewer['Blues'][7]

# Reverse color order so that dark blue is highest probability of violence
palette = palette[::-1]

# Add hover tool
hover = HoverTool(tooltips = [('Country','@country'),
                              ('Current leader', '@leader'),
                              ('Leader tenure (months)', '@tenure_months'),
                              ('Regime type', '@government'),
                              ('Election date', '@dates'),
                              ('Risk of election violence', '@logpredict')])

# Call the plotting function
p = make_plot(input_field)

# Make a slider object: slider 
slider = Slider(title = 'Months ahead', start = 1, end = 12, step = 1, value = 1)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
# Display the current document
layout = column(p, widgetbox(slider))
curdoc().add_root(layout)

# Save file
#output_file('election_violence_map.html')
#show(layout)
