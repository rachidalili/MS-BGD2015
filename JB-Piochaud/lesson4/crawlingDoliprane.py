# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 08:46:47 2015

@author: jean-baptiste
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"

#page:1
#affliste:0
#affNumero:0
#isAlphabet:0
#inClauseSubst:0
#nomSubstances:
#typeRecherche:0
#choixRecherche:medicament
#txtCaracteres:doliprane
#radLibelle:2
#txtCaracteresSub:
#radLibelleSub:4

params = {'page': 1, 'affliste': 0, 'affNumero' : 0,
        'isAlphabe' :0, 'inClauseSubst' : 0, 'nomSubstances' : '',
        'choixRecherche' : 'medicament', 'txtCaractere' : 'doliprane', 
        'radLibelle' : 2, 'txtCaracteresSub' : '', 'radLibelleSub' : 4}

def getSoupFromUrl(url):
    #request = requests.get(url)
    r = requests.post(url, data = params)
    #print(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
    
#def medicament(soup):
#    regex = re.compile(r'[0-9]{4}')
    
    
def main():
    soup = getSoupFromUrl(url)
    #table = soup.findAll('table', attrs= {'class' : 'standrat'})
    table = soup.findAll({'class' : 'standrat'})
    table = soup.findAll(class_="standart")
    table = pd.Series(table)
    type(table)
    #reg_string = r'(\d+)'
    #reg = re.compile(reg_string)
    #table.str.findall(reg)
    #res = table.str.findall(reg)
    #print(table)
    

if __name__ == '__main__':
    main()