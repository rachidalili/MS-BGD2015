# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 02:30:35 2015

@author: florian
"""

# coding: utf8
  
import requests
from bs4 import BeautifulSoup

def extractIntFromText(text):
  return int(text.replace('\xa0', '').replace(' ',''))


def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractionDesComptes(soup,position): 
    ListeParHbtsetParStrate=[]
    resultatParHabitant=soup.select("tr:nth-of-type(" + str(position) + ") > td:nth-of-type(2)")[0].text
    ListeParHbtsetParStrate.append(extractIntFromText(resultatParHabitant))
    resultatParStrate=soup.select("tr:nth-of-type(" + str(position) + ") > td:nth-of-type(3)")[0].text
    ListeParHbtsetParStrate.append(extractIntFromText(resultatParStrate))
    return ListeParHbtsetParStrate


ANNEE = [2010,2011,2012,2013]
COMPTESEXTRAITS={}

for anneeDeCompte in ANNEE:
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(anneeDeCompte)
    soup = getSoupFromUrl(url)
    ListeDesComptesParAnnee ={}
    ListeDesPositionsDansLaPageWeb = {"A":10,"B":14,"C":22,"D":27}
    
    for LigneDeCompte,NumeroDeCellule in ListeDesPositionsDansLaPageWeb.items():
        ListeDesComptesParAnnee[LigneDeCompte + " par habitant"]=extractionDesComptes(soup,NumeroDeCellule)[0]
        ListeDesComptesParAnnee[LigneDeCompte + " par strate"]=extractionDesComptes(soup,NumeroDeCellule)[1]
        
    COMPTESEXTRAITS[anneeDeCompte] = ListeDesComptesParAnnee

print(COMPTESEXTRAITS)