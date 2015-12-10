# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:29:05 2015
@author: cgilbert
"""
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getContentFromUrl(url):
	# Execute a request to get the content from a web page
	request = requests.get(url)
	# Parse the document
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

#def lienFromUrl(url)

url='http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&q=Renault+Zo%C3%A9'

def getLienFromUrl(url):
    soup = getContentFromUrl(url);
    list_bloc=soup.find("div", { "class" : "list-lbc" })
    list_article=list_bloc.findAll('a',href=True)
    liste_lien=[]
    for article in list_article:
        lien=str(article['href'])
        liste_lien.append(lien)
    return liste_lien

liste_lien=getLienFromUrl(url)

def getVersionFromSoup(soup_lien):
    content=str(soup_lien.find("div", { "class" : "content" }))
    searchObjVersion = re.search( r'intens|life|zen', content, re.M|re.I)
    if not(searchObjRenault is None):
        version=(searchObjVersion.group()).lower()
    else:
        version="version non renseignée"
    return version

def getPriceFromSoup(soup):
    price=soup.find("div", { "class" : "lbcParams withborder" }).find("span", { "class" : "price" })
    return(str(price['content']))

def getDateFromSoup(soup):
    release_date=soup.find("div", { "class" : "lbcParams criterias" }).find("td", { "itemprop" : "releaseDate" }).string
    return str(int(release_date))

def getKmFromSoup(soup):
    km_dirty=soup.find("div", { "class" : "lbcParams criterias" }).findAll("td")[3].string
    km=km_dirty.replace(" ","").replace("KM","")
    return km

def getSellerFromSoup(soup):
    param=soup.find("div", { "class" : "upload_by" }).find("span", { "class" : "ad_pro" })
    if param is None:
        seller='particulier'
    else:
        seller='pro'
    return seller

def getCoteFromVersionDate(version,date):
        non_decimal = re.compile(r'[^\d.]+')
        url_cote='http://www.lacentrale.fr/cote-auto-renault-zoe-'+version+'+charge+rapide-'+date+'.html'
        soup_dirty=getContentFromUrl(url_cote)
        cote_dirty=soup_dirty.find("span", { "class" : "Result_Cote arial tx20" }).string
        return(non_decimal.sub('', cote_dirty))
    




result_search=[]

for lien in liste_lien:
    
    soup_lien=getContentFromUrl(lien)
    titre=str(soup_lien.find("div", { "class" : "header_adview" }))    
    searchObjRenault = re.search( r'renault|zoe|zoé', titre, re.M|re.I)
    
    if not(searchObjRenault is None):
        
        version=getVersionFromSoup(soup_lien)
        price=getPriceFromSoup(soup_lien)
        km=getKmFromSoup(soup_lien)
        date=getDateFromSoup(soup_lien)
        seller=getSellerFromSoup(soup_lien)
        cote=getCoteFromVersionDate(version,date)

        
        for i in range(len(versions)):
            if(version==versions[i]):
                cote=cotes[i]
                
            if price>cote:
                commentaire='oui'
            elif price<cote:
                commentaire='non'
            else:
                commentaire='égal'
                
        
        info=[version,price,km,date,seller,cote,commentaire]
        result_search.append(info)
    
df = pd.DataFrame(result_search)
df.columns = ['version', 'prix (euros)','kilométrage','année','type de vendeur','cote','prix > cote ?']
df



# url_zoe='http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2013.html'
# soup_zoe_dirty=getContentFromUrl(url_zoe)
# cote_zoe_dirty=soup_zoe.find("span", { "class" : "Result_Cote arial tx20" }).string
# non_decimal = re.compile(r'[^\d.]+')
# cote_zoe = non_decimal.sub('', cote_zoe))
# url='http://www.leboncoin.fr/voitures/827471549.htm?ca=12_s'
# soup = getContentFromUrl(url)

# def getSellerFromSoup(soup):
#     param=soup.find("div", { "class" : "upload_by" }).find("span", { "class" : "ad_pro" }).string
#     if param is None:
#         seller='particulier'
#     else:
#         seller='pro'
        
#     return seller
    