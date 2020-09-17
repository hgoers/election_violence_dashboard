#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 15:15:27 2020

@author: hgoer
"""

# Import libraries
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from datetime import date

# Read in ELVIS data
df_elvis = pd.read_csv('https://raw.githubusercontent.com/OEFDataScience/REIGN_Dashboard/dd4b14f8172651a720f686b0f1bfbc3cc3a777c3/elvis_master_sept2019_final.csv')
df_elvis = df_elvis.set_index('Unnamed: 0')

# Clean ELVIS data
df_elvis = df_elvis[['country', 'dates', 'l.elecViolence2', 'regimetenure', 'pcgdp', 
                     'growth', 'logIMR', 'lnpop2', 'SPI', 'lexconst', 'lpolity2', 
                     'lpolcomp', 'political_violence', 'gov_democracy', 'gov_interim', 
                     'dem_duration']]
df_elvis['dates'] = pd.to_datetime(df_elvis['dates'])

# Read in election date data
df_dates = pd.read_csv('https://raw.githubusercontent.com/hgoers/election_dates_database/master/Election_dates.csv')

# Clean election date data
df_dates = df_dates[df_dates['date']!='None']
df_dates['date'] = pd.to_datetime(df_dates['date'])

df_dates_update = df_dates[df_dates['date']>date.today()]

# Set up the data for models
X = df_elvis[['regimetenure', 'pcgdp', 'growth', 'logIMR', 'lnpop2', 'SPI', 
              'lexconst', 'lpolity2', 'lpolcomp', 'political_violence', 'gov_democracy', 
              'gov_interim', 'dem_duration']]
y = df_elvis[['l.elecViolence2']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=101)

# Logistic regression
log_reg = LogisticRegression(C=1e6)
log_reg.fit(X_train, y_train)

# Predict the probability of violence
df_elvis['pred_vio'] = log_reg.predict_proba(X)[:,1]

# Make inforamed dummy data
