# coding: utf8
import requests
import random
import sys
from threading import Thread
import time
import os
import re
from bs4 import BeautifulSoup
import pandas as pd

payload = { 'page':1
    ,'affliste':0
    ,'affNumero':0
    ,'isAlphabet':0
    ,'inClauseSubst':'("00382","00382")'
    ,'nomSubstances':'(unable to decode value)'
    ,'typeRecherche':0
    ,'choixRecherche':'medicament'
    ,'txtCaracteres':'doliprane'
    ,'btnMedic.x':14
    ,'btnMedic.y':17
    ,'btnMedic': 'Rechercher'
    ,'radLibelle':2
    ,'txtCaracteresSub': ''
    ,'radLibelleSub':4
    }


def getSoupFromUrl(url):
  request = requests.post(url, data = payload)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

soup = getSoupFromUrl('http://base-donnees-publique.medicaments.gouv.fr/index.php#result')
names = [ x.text for x in soup.findAll('a', {'class':'standart'})]
names = pd.Series(names)
names = names.str.strip()
print names

reg_string = r'(\d+,?\d*) (\w+|), (\w+)'
reg = re.compile(reg_string)

res =  names.str.findall(reg)
print res


