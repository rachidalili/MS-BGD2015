# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:56:29 2015

@author: Jade
"""

#exo2 crawling
#e résultat des comptes de la ville de Paris pour les exercices 2009 à 2013
#récupérer les données A,B,C et D sur les colonnes Euros par habitant et par strate
#exemple rapport de 2013
#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013


# coding: utf8

import requests 
#inspection de l'element e.g "watch "texte, transformé en DOM
from bs4 import *
# coding: utf8

import requests #inspection de l'element "watch texte, transformé en DOM
from bs4 import BeautifulSoup 

#about BeautifulSoup
#Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping. Three features make it powerful:
#Beautiful Soup provides a few simple methods and Pythonic idioms for navigating, searching, and modifying a parse tree: a toolkit for dissecting a document and extracting what you need. It doesn't take much code to write an application
#Beautiful Soup automatically converts incoming documents to Unicode and outgoing documents to UTF-8. You don't have to think about encodings, unless the document doesn't specify an encoding and Beautiful Soup can't detect one. Then you just have to specify the original encoding.
#Beautiful Soup sits on top of popular Python parsers like lxml and html5lib, allowing you to try out different parsing strategies or trade speed for flexibility.
def getReport():
    year = str(year)
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
    return url

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

#test only one year's report first
soup = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2011')


  #average amount of strat
  #e.g from inspect element <td class="montantpetit G">2 308&nbsp;</td>


produitAChampStrat = soup.findAll("td", { "class" : "montantpetit G"})
produitAChampEuroPar = soup.findAll("td", { "class" : "montantpeitit G>2" })
produitAChampEuroPar = soup.findAll("td", { "class" : "montantpeitit G>5" })
  
print (produitAChampStrat)        #ok but lots of them ...
  
  #ask soup to read until it comes accross "TOTAL DES PRODUITS DE FONCTIONNEMENT A".
  
#"then extract only the amount that contains  only numbers per line of the 3 last read lines
 #<td class="montantpetit G">5 234 622&nbsp;</td>
  #<td class="montantpetit G">2 308&nbsp;</td>
  #<td class="montantpetit G">2 308&nbsp;</td>
  #<td class="libellepetit G">TOTAL DES PRODUITS DE FONCTIONNEMENT = A</td>
  
  #Same logic for B, C and D
  #<td class="libellepetit G">TOTAL DES CHARGES DE FONCTIONNEMENT = B</td>
  #etc...
  




