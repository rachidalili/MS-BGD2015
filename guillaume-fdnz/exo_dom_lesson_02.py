# coding: utf8

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractParisData(url):

  compteCategorie = {}
  comptesToutesCategories = []
  #Indices des balises td de la page web pour chaque premier élément de categorie 
  firstIndexDict = {'A': 1, 'B': 4, 'C': 10, 'D': 13}

  soup = getSoupFromUrl(url)
  montantsComptes = soup.findAll("td", { "class" : "montantpetit G" })
  
  for category, firstIndex in firstIndexDict.iteritems():     
      compteCategorie['categorie'] = category
      compteCategorie['hab'] = montantsComptes[firstIndex].text
      compteCategorie['strate'] = montantsComptes[firstIndex+1].text
      comptesToutesCategories.append(compteCategorie.copy()) #On ajoute une copie sinon, on ajoute uniquement la référence. seul le dernier élément est référencé  
  return comptesToutesCategories
  
def displayBeautifulData(ComptesToutesCategories):
    for CompteCategorie in ComptesToutesCategories:
        print "<-----",CompteCategorie['categorie'],"----->"
        print "Euros/hab: ",CompteCategorie['hab']
        print "Euros/strate",CompteCategorie['strate']
      
url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013"
ComptesToutesCategories = extractParisData(url)
displayBeautifulData(ComptesToutesCategories)