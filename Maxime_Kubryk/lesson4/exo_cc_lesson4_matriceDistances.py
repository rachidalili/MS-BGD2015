from itertools import product
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import itertools


villes = pd.read_csv('villes.csv')

print(villes.head(10))

data = pd.DataFrame(list(product(villes['Ville'].values, villes[
                    'Ville'].values)), columns=['origin', 'dest'])

print(data.head(10))

for row in data.values:
    print(row)

    answer = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins=' +
                          row[0] + '&destinations=' + row[1])

    answer = answer.json()

    print(answer['rows'][0]['elements'][0]['distance']['text'])
