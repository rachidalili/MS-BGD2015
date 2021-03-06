from sklearn import linear_model
import numpy as np
import pandas
import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import urllib, json
import pprint



cheminCSV = '/Users/williambenhaim/ProjetMSBigData/MS-BGD2015/Lessons-Exercices/villes.csv'
data = pd.read_csv(cheminCSV, sep=',')
villes=data['Ville']
mytoken = 'AIzaSyDWg78VWNp8ROgTUZDt8rKGVXMf9R98p5U'
def extract_value(row):
  return map( lambda x: x['duration']['text'], row['elements'])

alldistance=[]
distance=[]
ville=[]
for villeA in villes[0:10]:
	distance=[]
	for villeB in villes[0:10]:
		mapp = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+villeA+'&destinations='+villeB+'&language=fr-FR&key='+mytoken
		googleResponse = urllib.urlopen(mapp)
		jsonResponse = json.loads(googleResponse.read())
		distance.append(jsonResponse['rows'][0]['elements'][0]['distance']['value'])
	alldistance.append(distance)
	ville.append(villeA)

Result_DF = pd.DataFrame(alldistance, columns=ville,index=ville)