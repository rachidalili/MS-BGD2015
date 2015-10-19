# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import requests
from bs4 import BeautifulSoup

year = ['2010', '2011', '2012', '2013']

def getUrl(year):
    year = str(year)
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
    return url

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
  
