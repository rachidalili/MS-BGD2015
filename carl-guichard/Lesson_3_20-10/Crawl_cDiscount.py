# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:34:20 2015

@author: Carl
"""

# Exercice cours : récupérer nom des produits, images, ancien et nouveau prix
# sur une page cdiscount
# on travaille sur : http://www.cdiscount.com/ct-ordinateurs-portables/acer+aspire.html#_his_

# On utilise les bibliothèques python suivantes :
#   - requests ==> pour faire des requêtes HTTP et récupérer les pages HTML qui nous intéressent
#   - beautifulSoup ==> pour parser le HTML et y récupérer des éléments précis

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

# definir les objets recherchés
ordinateur = 'acer aspire'
wordList = ordinateur.split()

# prendre l'url et le mettre dans une soupe
# url de base
urlBase = "http://www.cdiscount.com/"
urlRecherche = urlBase + "/search/10/" + wordList[0] + "+" + wordList[1] + ".html#_his_"
soup = getSoupFromUrl(urlRecherche)
#print html.prettify()
blocs = soup.find_all('div', {'class': 'prdtBloc'})
for bloc in blocs:
    html = bloc.find('a').get('href')
    descr = bloc.find('p', {'class': 'prdtBDesc'}).text.encode('utf-8')
    price = bloc.find('span',{'class':'price'}).text.encode('utf-8')
    print html
    print descr
    print price












