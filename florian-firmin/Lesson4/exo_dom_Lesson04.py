# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:28:53 2015

@author: florian
"""

"""
L'objectif est de générer un fichier de données sur le prix des Renault Zoé 
sur le marché de l'occasion en Ile de France, PACA et Aquitaine. 
Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir 
les infos suivantes : version ( il y en a 3), année, kilométrage, prix, 
téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle 
que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.
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


# GESTION DE L4ARGUS
urlargus="http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html"
soupargus = getSoupFromUrl(urlargus)
dicoargus={}
entries=soupargus.find("div",{"id" : "listing_quot"}).find_all("a",{"style" : "color:#007EFF; text-decoration:underline"})
for entry in entries:
    soupargusmodele = getSoupFromUrl("http://www.lacentrale.fr/"+entry["href"])
    coteargus=extractIntFromText(soupargusmodele.find("span",{"class":"Result_Cote arial tx20"}).text[:-2])
    dicoargus[entry.text]=coteargus
coteArgusData=pd.DataFrame(dicoargus,index=["cote argus"]).T

etudefinale = pd.merge(ZoeLeBoncoin,coteArgusData,left_on="version",right_index=True,how="left" )
etudefinale['position_argus']=etudefinale.apply(lambda x:"supérieur à l'argus" if x["prix"]>x["cote argus"] else "inferieur à l'argus",axis=1)
print (etudefinale)
 
    

        
        
        
    
    