from sklearn import linear_model                  
import numpy as np
import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import urllib, json
import pprint


def removeSpecialCarFromText(text):
	return text.replace(u'\xc2', u'').replace(u'\xa0', u'').replace(u'\xe2', u'').replace(u'\x82', u'').replace(u'\xac', u'').replace(u'\u20ac', u'').replace(u'\n', u'')


data_df = pandas.read_csv('/Users/lucasweissert/MS-BGD2015/Lessons-Exercices/villes.csv', sep = ',')

print data_df

villes = data_df['Ville']
# Departement = data_df['Departement']

url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=AIzaSyDLdf1PFF0DpZaRJjHUm52HPAmWH9ZxwIk'
print url

dests = villes[0:10]
for ville in villes[0:10]:
	print ville
	for dest in dests:
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + ville + '&destinations=' + dest +'&mode=bicycling&language=fr-FR&key=AIzaSyDLdf1PFF0DpZaRJjHUm52HPAmWH9ZxwIk'
		googleResponse = urllib.urlopen(url)
		jsonResponse = json.loads(googleResponse.read())
		print ville + ' to ' + dest + ' : ' + removeSpecialCarFromText(jsonResponse['rows'][0]['elements'][0]['distance']['text'])