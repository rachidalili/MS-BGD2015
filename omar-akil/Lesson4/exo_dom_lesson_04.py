
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getContentFromUrl(url):
	r = requests.get(url)
	s = BeautifulSoup(request.text, 'html.parser')
	return soup


url='http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&q=Renault+Zo%C3%A9'

def getLienFromUrl(url):
    s = getContentFromUrl(url);
    list_bloc=s.find("div", { "class" : "list-lbc" })
    list_article=list_bloc.findAll('a',href=True)
    list_lien=[]
    for article in list_article:
        lien=str(article['href'])
        list_lien.append(lien)
    return list_lien

list_lien=getLienFromUrl(url)

def getVersionFromSoup(sl):
    co=str(sl.find("div", { "class" : "content" }))
    searchVersion = re.search( r'intens|life|zen', content, re.M|re.I)
    if not(searchRenault is None):
        version=(searchVersion.group()).lower()
    else:
        version="version non identifiée"
    return version

def getPriceFromSoup(s):
    price=s.find("div", { "class" : "lbcParams withborder" }).find("span", { "class" : "price" })
    return(str(price['content']))

def getDateFromSoup(s):
    release_date=s.find("div", { "class" : "lbcParams criterias" }).find("td", { "itemprop" : "releaseDate" }).string
    return str(int(release_date))

def getKmFromSoup(s):
    km_dirty=s.find("div", { "class" : "lbcParams criterias" }).findAll("td")[3].string
    km=km_dirty.replace(" ","").replace("KM","")
    return km

def getSellerFromSoup(s):
    param=s.find("div", { "class" : "upload_by" }).find("span", { "class" : "ad_pro" })
    if param is None:
        seller='particulier'
    else:
        seller='professionnel'
    return seller

def getCoteFromVersionDate(version,date):
        no_decimal = re.compile(r'[^\d.]+')
        url_cote='http://www.lacentrale.fr/cote-auto-renault-zoe-'+version+'+charge+rapide-'+date+'.html'
        soup_1=getContentFromUrl(url_cote)
        cote_1=soup_1.find("span", { "class" : "Result_Cote arial tx20" }).string
        return(no_decimal.sub('', cote_dirty))
    




result_search=[]

for lien in list_lien:
    
    sl=getContentFromUrl(lien)
    titre=str(sl.find("div", { "class" : "header_adview" }))    
    searchRenault = re.search( r'renault|zoe|zoé', titre, re.M|re.I)
    
    if not(searchRenault is None):
        
        version=getVersionFromSoup(sl)
        price=getPriceFromSoup(sl)
        km=getKmFromSoup(sl)
        date=getDateFromSoup(sl)
        seller=getSellerFromSoup(sl)
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


    