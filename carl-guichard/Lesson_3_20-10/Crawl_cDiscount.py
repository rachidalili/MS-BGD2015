# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:34:20 2015

@author: Carl
"""

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

# definir les objets recherchés
ordinateur = 'Dell XPS 15'
wordList = ordinateur.split()

# prendre l'url et le mettre dans une soupe
# url de base
urlBase = "http://www.cdiscount.com/"
urlRecherche = urlBase + "/search/10/" + wordList[0] + "+" + wordList[1] + "+" +  wordList[2] + ".html#_his_"
html = getSoupFromUrl(urlRecherche)
print html