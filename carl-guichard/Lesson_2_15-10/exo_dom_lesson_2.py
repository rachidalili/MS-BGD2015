# coding: utf8

import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup


def extractMetrics(string, length):
  # on cherche la première classe qui a un libelle correspondant a la question
  class1 = soup.find("td",{"class":"libellepetit G"})
  if (class1 == None):
    #Si elle n'existe pas : pas de de donnée pour l'année en cours    
    print  "Pas de données pour cette année" 
    return 
  for i in range ((length+1)):
      #On recherche le libellé de la question dans la classe
      if (string in class1.next_element):
        print "=========================================="
        print class1.next_element
        # on cherche la classe précédente avec le montant de la strate
        class2 = class1.find_previous("td",{"class":"montantpetit G"})
        print "Moyenne de la strate : " + class2.next_element
        # Et Encore la précédente pour trouver l'euro par habitant       
        class3 = class2.find_previous("td",{"class":"montantpetit G"})
        print "Euros par habitants : " + class3.next_element
        print "=========================================="
        #on passe a la classe suivante      
      class1 = class1.find_next("td",{"class":"libellepetit G"})
  return 


# Main

years = ["2009","2010","2011","2012","2013"]
year = ""

ligne = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
"TOTAL DES CHARGES DE FONCTIONNEMENT = B",
"TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
"TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]


for year in enumerate (years):
  print  "\n" + year[1] + "\n"
  url= "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+ year[1]
  soup = getSoupFromUrl(url)
  for i in range(len(ligne)):
    extractMetrics(ligne[i],len(ligne))
