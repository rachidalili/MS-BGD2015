# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:29:46 2015

@author: Carl
"""

import pandas as pd

import googlemaps

path = "/Users/Carl/Documents/MyDocuments/Universites/Cours/Telecom_paristech/Git/MS-BGD2015/MS-BGD2015/Lessons-Exercices"

my_data = pd.read_csv(path + '/villes.csv')

api_key = 'AIzaSyB2ilmg-jMnKJMLj9kiwY658ZUHJbOg4JA'
gmaps = googlemaps.Client(key=api_key)

origins = list(my_data['Ville'].values[0:10])
destinations = list(my_data['Ville'].values[0:10])

print origins
print destinations

