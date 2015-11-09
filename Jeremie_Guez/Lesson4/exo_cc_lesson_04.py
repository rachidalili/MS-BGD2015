# encoding: utf-8

import pandas as pd
import urllib2
import json

data = pd.read_csv('villes.csv')

data_out = pd.DataFrame(columns=['Départ', 'Arrivée', 'Distance'])

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"
api_key = 'AIzaSyCo0R6D3t2h7WXupJwTn7XJikFgw8vMqSs'
destinations = ''

for reci in data.values:
    for recj in data.values:
        if recj[0] != reci[0]:
            query = url + '&origin=' + reci[0] + ' ' + reci[1] + ' France'
            query += '&destinations=' + recj[0] + ' ' + recj[1] + ' France'
            query += '&key=' + api_key
            print query
            response = json.loads(urllib2.urlopen(query).read())
            print response
            data_out.append({
                'Départ': reci[0],
                'Arrivée': recj[1],
                'Distance': response['rows'][0]['distance']['value']
            })

print data_out
