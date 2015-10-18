# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 23:21:50 2015

@author: kim
"""

import sys, os
from lxml import html
import requests
from bs4 import BeautifulSoup
print requests.__version__
import json
import re


def getmetrics( soup ):   
    tile_links = soup.findAll("tr", { "class" : "bleu" })[0]
    #print tile_links
    sub_tile_links = soup.findAll("td", { "class" : "montantpetit G" })   
    print "Euros par habitant pour A: ",sub_tile_links[1].text
    print "Moyenne de la strate pour A: ",sub_tile_links[2].text
    print "Euros par habitant pour B: ",sub_tile_links[4].text
    print "Moyenne de la strate pour B: ",sub_tile_links[5].text
    print "Euros par habitant pour C: ",sub_tile_links[10].text
    print "Moyenne de la strate pour C: ",sub_tile_links[11].text
    print "Euros par habitant pour D: ",sub_tile_links[13].text
    print "Moyenne de la strate pour D: ",sub_tile_links[14].text

liste_annees = ["2010", "2011", "2012","2013"]
#liste_annees = ["2012"]
for i in range(len(liste_annees)): 
    print "Donnees pour l'annee: ", liste_annees[i]
    url = u'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+liste_annees[i]
    #print url
    r = requests.get(url,  stream=True)
    soup = BeautifulSoup(r.text) ## when using requests.get
    getmetrics(soup)

