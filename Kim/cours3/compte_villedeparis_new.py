# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:19:24 2015

@author: kim
"""
import requests
from bs4 import BeautifulSoup


def fromUrltoSoup( url):
    r = requests.get(url,  stream=True)
    return BeautifulSoup(r.text, 'html.parser')
    

def getmetrics( soup ):    
    print "****************Nouvelle version*********************"    
    for i in libelle_nums: 
        print "Euros par hab. A: ",soup.select('tr:nth-of-type('+ str(i) + ') > td:nth-of-type(2)')[0].text
        print "Moyenne de la strate A: ",soup.select('tr:nth-of-type('+ str(i) + ') > td:nth-of-type(3)')[0].text
   
    print "****************Ancienne version*********************"
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
libelle_nums = [10, 14, 22, 27]
for j in range(len(liste_annees)):    
    print " \n\n"
    print "Donnees pour l'annee: ", liste_annees[j]
    url = u'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+liste_annees[i]
    fromUrltoSoup( url) 
    getmetrics(fromUrltoSoup( url))

