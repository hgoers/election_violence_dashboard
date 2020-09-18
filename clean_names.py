"""
Created on Thu Sep 17 17:27:33 2020
@author: hgoer
"""
def clean_names(df):        
    import pandas as pd
    import numpy as np

    # Catch weird countries
    clean_dict = {'Argentine Republic':'Argentina',
                  'East Timor':'Timor Leste',
                  'Timor-Leste':'Timor Leste',
                  'Democratic Republic of Timor-Leste':'Timor Leste',
                  'French Republic':'France',
                  'Gabonese Republic':'Gabon',
                  'Italian Republic':'Italy',
                  'Lao People\'S Democratic Republic':'Laos',
                  'Lao People\'s Democratic Republic':'Laos',
                  'Lao PDR':'Laos',
                  'Lebanese Republic':'Lebanon',
                  'Myanmar (Burma)':'Myanmar',
                  'Burma':'Myanmar',
                  'New Caledonia And Dependencies':'New Caledonia',
                  'DPRK':'North Korea',
                  'Portuguese Republic':'Portugal',
                  'Russian Federation':'Russia',
                  'Serbia (Yugoslavia)':'Serbia',
                  'Slovakia':'Slovak Republic',
                  'Surinam':'Suriname',
                  'Swiss Confederation':'Switzerland',
                  'Syrian':'Syria',
                  'Togolese Republic':'Togo',
                  'Tunisian Republic':'Tunisia',
                  'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                  'United Mexican States':'Mexico',
                  'United States Of America':'United States',
                  'Territory of New Caledonia and Dependencies':'New Caledonia',
                  'Turkish Republic of Northern Cyprus (TRNC)':'Northern Cyprus',
                  'Democratic Republic of the Congo':'DRC',
                  'Democratic Republic of Congo':'DRC',
                  'Hellenic Republic':'Greece',
                  'USA':'United States of America'}
    df = df.replace(clean_dict)

    # Remove common formal names
    common_dict = {'Commonwealth of the':'',
                   'Commonwealth of':'',
                   'People\'s Democratic Republic of ':'',
                   'Democratic Socialist Republic of':'',
                   'Federal Democratic Republic of':'',
                   'Democratic Republic of':'',
                   'Federal Republic of':'',
                   'Federation of':'',
                   'Federative Republic of':'',
                   'Hashemite Kingdom of':'',
                   'Special Administrative Region':'',
                   'Independent State of':'',
                   'Islamic Republic of':'',
                   'Kingdom of the':'',
                   'Kingdom of':'',
                   'Oriental Republic of':'',
                   'Overseas Lands of':'',
                   'People\'s Republic of ':'',
                   'Plurinational State of':'',
                   'Principality of':'',
                   'Grand Duchy of':'',
                   'Socialist Republic of':'',
                   'Sultanate of':'',
                   'Arab Republic of':'',
                   'Arab Republic':'',
                   'Territory of the':'',
                   'Territory of':'',
                   'Union of the':'',
                   'Union of':'',
                   'United Republic of':'',
                   'Autonomous Community of':'',
                   'Bolivarian Republic of':'',
                   'Cooperative Republic of':'',
                   'Republic of the':'',
                   'Country of':'',
                   'State of':'',
                   'Republic of':''}
    
    df = df.replace(common_dict, regex=True)
    
    # Remove leading and trailing spaces
    df = df.str.strip()

    return df
