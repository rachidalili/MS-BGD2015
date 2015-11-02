# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:28:53 2015

@author: florian
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
def extractIntFromText(text):
  return int(text.replace(" ",""))

ZoeLeBoncoin = pd.DataFrame(columns = ['titre', 'reg', 'version', 'année','km','prix','tél','vendeur','argus'])

typeAcheteur  = {"professionnel":"c","particulier":"p"}
region = ["ile_de_france","provence_alpes_cote_d_azur","aquitaine"]
  
url_liste = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=zoe&f=c'
soup = getSoupFromUrl(url_liste)
uneAnnonce={}
uneAnnonceList=[]

entries = soup.find("div", { "class" : "list-lbc" }).find_all("a")  
for entry in entries:
    if "zoe" in entry['title'].lower():
        uneAnnonce["titre"]=entry['title']
        uneAnnonce["region"]="ile de France"
        uneAnnonce["type vendeur"]="Pro"
        url_annonce = entry['href']
        soupAnnonce = getSoupFromUrl(url_annonce)
        uneAnnonce["prix en euros"] = int(soupAnnonce.find("div", { "class" : "lbcParams withborder" }).find("span", { "class" : "price" })['content'])        
        uneAnnonce["année"] = int(soupAnnonce.find("div", { "class" : "lbcParams criterias" }).find("td", { "itemprop" : "releaseDate" }).get_text())
        uneAnnonce["kimometrage"] = extractIntFromText(soupAnnonce.find("div", { "class" : "lbcParams criterias" }).select("tr:nth-of-type(3) > td:nth-of-type(1)")[0].text[:-3])
        
        uneAnnonce["description"]=soupAnnonce.find("div", { "itemprop" : "description"}).get_text()        
        if "life" in uneAnnonce["description"].lower():
            uneAnnonce["version"]="LIFE CHARGE RAPIDE"
        elif "intens" in uneAnnonce["description"].lower():
            uneAnnonce["version"]="INTENS CHARGE RAPIDE"    
        elif "zen" in uneAnnonce["description"].lower():
            uneAnnonce["version"]="ZEN CHARGE RAPIDE"
        else:
            uneAnnonce["version"] = "VERSION INCONNUE"
        
        uneAnnonceList = pd.DataFrame({'titre':uneAnnonce["titre"],'reg':uneAnnonce["region"],'version':uneAnnonce["version"],'année':uneAnnonce["année"],'km':uneAnnonce["kimometrage"],'prix':uneAnnonce["prix en euros"],'tél':"",'vendeur':uneAnnonce["type vendeur"],'argus':""},index=[0])      
        ZoeLeBoncoin=pd.concat([ZoeLeBoncoin,uneAnnonceList])
        ZoeLeBoncoin.reset_index()

print (ZoeLeBoncoin)
        
        
        
    

        
        
        
    
    