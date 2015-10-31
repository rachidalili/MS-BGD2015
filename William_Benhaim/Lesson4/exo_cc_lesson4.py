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



def connectWithToken():
    request = requests.get(github_api_url + "/user", headers=rqHeader)
    return request.status_code

cheminCSV = '/Users/williambenhaim/ProjetMSBigData/MS-BGD2015/Lessons-Exercices/villes.csv'
data = pd.read_csv(cheminCSV, sep=',')
villes=data['Ville']
mytoken = 'AIzaSyDWg78VWNp8ROgTUZDt8rKGVXMf9R98p5U'


for villeA in villes[0:10]:
	for villeB in villes[0:10]:
		tt=1
mapp = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Paris&destinations=Poitier&mode=bicycling&language=fr-FR&key=AIzaSyDWg78VWNp8ROgTUZDt8rKGVXMf9R98p5U'

googleResponse = urllib.urlopen(mapp)
jsonResponse = json.loads(googleResponse.read())
#mapp = 'https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=' + mytoken
resp = requests.get(mapp)
datta = json.loads(resp.text)
datta= datta['rows']
