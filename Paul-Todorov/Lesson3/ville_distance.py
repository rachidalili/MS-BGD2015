import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import googlemaps

API_KEY = 'AIzaSyBa9OpLmiqOqJeL9mFjfSGlRd6cQgrOyiA' 

gmaps = googlemaps.Client(key=API_KEY)


cities = pd.read_csv('villes.csv')

origins=  list(cities['Ville'].values[0:10])
destinations = list(cities['Ville'].values[0:10])


matrix = gmaps.distance_matrix(origins,destinations)
matrix_marche = gmaps.distance_matrix(origins, destinations,mode='walking')


def extract_value(row):
	return map( lambda x : x['distance']['text'], row['elements'])


mn = map(extract_value, matrix['rows'])
mn_marche = map(extract_value, matrix_marche['rows'])


duree = DataFrame(mn, index = origins, columns = destinations)
duree_marche = DataFrame(mn_marche, index = origins, columns = destinations)