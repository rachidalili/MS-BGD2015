__author__ = 'Mohamed Amine'
import pandas as pd
import requests
import numpy as np


key = 'AIzaSyAW3ZPrd47VgUv4SyNmtlFgxrV-1oKRLPg'
paths = pd.read_csv('D:/Projects/Python/MS-BGD2015/Lessons-Exercices/villes.csv')

paths = paths.head(10)

#print paths[['Ville']]

def get_soup_for_page(origin,destination):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+'+FR&destinations='+destination+'+FR&mode=bicycling&language=fr-FR&key=AIzaSyAW3ZPrd47VgUv4SyNmtlFgxrV-1oKRLPg'

    print url
    page = requests.get(url)
    return page.json()

print get_soup_for_page('paris', 'paris')['rows'][0]['elements'][0]['distance']['text']

matrix =[]
for ville in np.asarray(paths[['Ville']]):
    line=[]
    for ville2 in np.asarray(paths[['Ville']]):
        print ville + " " + ville2
        aa = get_soup_for_page(ville[0], ville2[0])['rows'][0]['elements'][0]['distance']['text']
        print aa
        line.append(aa)
    matrix.append(line)

pdmat= pd.DataFrame(np.asarray(matrix), index = np.asarray(paths[['Ville']]), columns = np.asarray(paths[['Ville']]))
print pdmat.head(10)
