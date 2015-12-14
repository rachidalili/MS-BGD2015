# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 20:09:42 2015

@author: varieux
"""

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re

import googlemaps

API_KEY = 'AIzaSyAcXNyjXepUbFyAf5auZq_RAF_CJJofG_E'

#create the Google maps client
gmaps = googlemaps.Client(key=API_KEY)

# read the cities

cities = pd.read_csv('villes.csv')

origins = ["Perth, Australia", "Sydney, Australia",
                   "Melbourne, Australia", "Adelaide, Australia",
                   "Brisbane, Australia", "Darwin, Australia",
                   "Hobart, Australia", "Canberra, Australia"]

origins = list(cities['Ville'].values[0:10])
destinations = list(cities['Ville'].values[0:10])

matrix = gmaps.distance_matrix(origins, destinations)
matrix_train = gmaps.distance_matrix(origins, destinations,mode='walking')


def extract_value(row):
  return map( lambda x: x['duration']['text'], row['elements'])

mm = map(extract_value, matrix['rows'])
mm_train = map(extract_value, matrix_train['rows'])

dur = DataFrame(mm,index=origins, columns=destinations)
dur_train = DataFrame(mm_train,index=origins, columns=destinations)