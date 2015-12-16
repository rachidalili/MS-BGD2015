# coding: utf8

import pandas as pd
import json
import re
import requests
from bs4 import BeautifulSoup
#from pytesser import *

import requests
import json

def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup


headers = {'content-type': 'text/html'}
url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

data = {'choixRecherche':"medicament",
'page':"1",
'affliste':"0",
'affNumero':"0",
'isAlphabet':"0",
'inClauseSubst':"0",
'nomSubstances':"",
'typeRecherche':"0",
'txtCaracteres':"doliprane",

}

r = requests.post(url, data=data)

soup = BeautifulSoup(r.text,'html.parser')


liens = soup.findAll(attrs={'class':'standart'})

results =  pd.DataFrame([lien.text for lien in liens])


for result in results:
    print re.compile(r"(\d+,?\d*) (\w+),(\w+)").search(result).group()
#pd.value_counts(pd.cut(aliments[u'energy_100g'].dropna(),5))


traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])

camera.groupby(lambda x : x.split('')[0])['Weight'].mean().order()
