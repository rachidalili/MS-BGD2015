# coding: utf8
#from __future__ import unicode_literals 
#Phase 1: Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
#Phase 2: En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users
#le nombre moyens de stars des repositories qui leur appartiennent.
#Pour finir classer ces 256 contributors par leur note moyenne.

import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import googlemaps

#sourceVilles = 'https://raw.githubusercontent.com/rachidalili/MS-BGD2015/master/Lessons-Exercices/villes.csv'
sourceVilles = 'villes.csv'
data = pd.read_csv(sourceVilles)

print data.head()

# https://console.developers.google.com/project/apprendreapi/apiui/credential
APIkey = "AIzaSyAhkENdoR9bOpdq1qPpTa4073wSNQw6Lgs"

gmaps = googlemaps.Client(key=APIkey)

villes = list(data['Ville'].values[0:10])

origins = villes
destinations = villes

distanceMatrix = gmaps.distance_matrix(origins, destinations)

print distanceMatrix

def extract_values(row):
    map(lambda x: x['distance']['text'], row['elements'])

mm = map(extract_values, distanceMatrix['rows'])

distances = pd.DataFrame(mm, index=origins, columns=destinations)

#https://github.com/googlemaps/google-maps-services-python
#https://developers.google.com/maps/documentation/javascript/distancematrix
#exemple distance matrix https://github.com/googlemaps/google-maps-services-python/blob/master/test/test_distance_matrix.py
