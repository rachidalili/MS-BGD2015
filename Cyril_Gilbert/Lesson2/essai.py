# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 10:11:27 2015

@author: Cyril Gilbert
"""


import requests
from bs4 import BeautifulSoup

def extractIntFromText(text):
  intermediate_string=text.replace(u' ', u'')
  return int(intermediate_string.replace(u'\xa0', u''))
  
def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup


def what_line(table_line,ressource): #we assume there is only one str 'search' in table_line
    for line in table_line:    
        current_test=line.findAll("td", { "class" : "libellepetit G" })
        if current_test and current_test[0].text == ressource :
            good_line=line
            return good_line

metrics={};
years=range(2010,2015)
candidates = ['TOTAL DES PRODUITS DE FONCTIONNEMENT = A','TOTAL DES CHARGES DE FONCTIONNEMENT = B','TOTAL DES RESSOURCES D\'INVESTISSEMENT = C','TOTAL DES EMPLOIS D\'INVESTISSEMENT = D']

print('Quelques informations relatives aux comptes de la mairie de Paris : \n\n')

for year in years:
    soup=getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
            
    print('Année'+str(year)+' :\n')
    
    for candidate in candidates:
    
        table_line = soup.findAll("tr", { "class" : "bleu" })
        right_line=what_line(table_line,candidate)

        value_euros=extractIntFromText(right_line.findAll("td", { "class" : "montantpetit G" })[1].text)
        value_meanstrate=extractIntFromText(right_line.findAll("td", { "class" : "montantpetit G" })[2].text)

        metrics[candidate]=['Euros par habitant: '+str(value_euros),'Moyenne de la strate: '+str(value_meanstrate)]
        print(candidate+'\n '+metrics[candidate][0]+', '+metrics[candidate][1])
        
    print('\n \n')
