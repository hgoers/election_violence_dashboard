# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 13:51:27 2020

@author: hgoer
"""
# Import libraries
import pandas as pd

# Read in data
df = pd.read_csv('https://raw.githubusercontent.com/hgoers/election_violence_dashboard/master/upcoming_election_vio.csv')[['date', 'status', 'country', 'pred_vio']]

# Filter for upcoming elections
df['date'] = pd.to_datetime(df['date'])
df = df[df['date']>pd.to_datetime('today')]

# Ensure data is sorted with most recent first
df = df.sort_values(by=['date'])

