# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 23:51:48 2015

@author: Jade
"""

#import urllib2
from bs4 import BeautifulSoup
import requests
import re




url="http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&q=renault+zoe"





def getSoupFromUrl(url):
 #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

#soup = BeautifulSoup(html, 'html.parser')
soup = getSoupFromUrl(url)
print(soup)
tab_link =[]
for link in soup.find_all('a'):
    lien=link.get('href')
    title1=link.get('title')
    if title1 != None:
        m=re.findall('zoe',title1)
        if m != None:
            print (title1)
            tab_link.append(lien)

# pour chaque offre
for i in tab_link:
    print (i)
    soupi=getSoupFromUrl(i)
