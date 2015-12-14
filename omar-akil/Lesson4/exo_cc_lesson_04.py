"""
@author: omakil
"""

import pandas as pd
import requests
import json
from urllib.request import urlopen

data = pd.read_csv('villes2.csv')

df = pd.DataFrame(columns=['Depart', 'Arrivee', 'Distance'])

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"
api = 'AIzaSyBCUUmmy_DXyVzcpIKC49RV5qyuvmOOaQk'
# api a effacer
destinations = ''

for villei in data.values:
    for villej in data.values:
        if villej[0] != villei[0]:
            query = url + '&origins=' + villei[0] + ' ' + villei[1] + ' France'
            query += '&destinations=' + villej[0] + ' ' + villej[1] + ' France'
            query += '&key=' + api
            r=requests.get(query).json()
            result = json.loads(urlopen(query).read())

            df.append({
                'Depart': villei[0],
                'Arrivee': villej[1],
                'Distance': result['rows'][0]['elements'][0]['distance']['value']
            },ignore_index=True)

print(df)
