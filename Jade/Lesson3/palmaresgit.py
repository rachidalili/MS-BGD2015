# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 21:33:24 2015

@author: jade
"""

#Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
import requests 
#inspection de l'element e.g "watch "texte, transformé en DOM
from bs4 import BeautifulSoup
import pandas as pd


def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  

url = "https://gist.github.com/paulmillr/2657075"

soup = getSoupFromUrl(url)

i=0
score = []
nom =[]

for element in soup.find_all('tr',limit=257):
    if i>0:
        score.append(element.find('th').get_text())
        nom.append(element.find('td').get_text())
    i=i+1
   

param = pd.DataFrame({ 'contributeur' : nom} ) 
param.index +=1
param


