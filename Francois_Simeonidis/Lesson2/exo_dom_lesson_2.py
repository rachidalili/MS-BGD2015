# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:30:53 2015

@author: francois
"""

import requests
from bs4 import BeautifulSoup

def extractIntFromText(text):
  temp = text.replace(u'\xa0', u'')
  return int(temp.replace(' ', ''))


names = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
         "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
         "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
         "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]


def getValues(names, url):
    values = [None, None, None, None]
    request = requests.get(url)

    soup = BeautifulSoup(request.text, 'html.parser')

    for row in soup.find_all('tr', attrs={'class','bleu'}):
#       print('------',type(row),sep='|')
#       print(row)
    
        cells = row.findChildren('td')
    
#       pour les lignes qui ont plus de 4 colonnes...
        if (len(cells)>=4):
            descr = cells[3].string

#       ...si la 4ème colonne qui contient le nom de l'indicateur (ou autre chose) est reconnue comme un nom recherché
            if (descr in names):
                value = cells[1].string
                value = extractIntFromText(value)
#       ...on affecte la valeur de même rang de liste que l'indicateur trouvé
                values[names.index(descr)] = value
    return values
            

print (names)
for year in range (2009,2014):
    print(year,":",getValues(names,"http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+str(year)))
    
"""
['TOTAL DES PRODUITS DE FONCTIONNEMENT = A',
 'TOTAL DES CHARGES DE FONCTIONNEMENT = B',
 "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
 "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
2009 : [None, None, None, None]
2010 : [2449, 2241, 1119, 1265]
2011 : [2546, 2327, 1264, 1268]
2012 : [2311, 2135, 1085, 1058]
2013 : [2308, 2235, 1157, 1048]
>>> 

"""