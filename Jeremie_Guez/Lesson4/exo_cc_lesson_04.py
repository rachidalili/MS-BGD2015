# encoding: utf-8

import pandas as pd
from urllib.request import urlopen
import json

data = pd.read_csv('villes.csv')

data_out = pd.DataFrame(columns=['Départ', 'Arrivée', 'Distance'])

url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
api_key = 'AIzaSyC3i2ytEqL_eyH-x6cX4-QhuQyLVE3vik8'
destinations = ''

for reci in data.values:
    for recj in data.values:
        if recj[0] != reci[0]:
            query = url + 'origins=' + reci[0]
            query += '&destinations=' + recj[0] +'&mode=bicycling&language=fr-FR&'
            query += '&key=' + api_key
            #print (query)
            response = json.loads(urlopen(query).read().decode('utf-8'))
#            print(reci[0])
#            print(recj[0])
#            print(response['rows'][0]['elements'][0]['distance']['value'])
            data_out.append({
                'Départ': reci[0],
                'Arrivée': recj[0],
                'Distance': response['rows'][0]['elements'][0]['distance']['value']
            })
            
print (data_out)