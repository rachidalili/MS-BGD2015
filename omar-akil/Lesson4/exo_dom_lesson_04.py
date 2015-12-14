import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

#donnees
url='http://www.leboncoin.fr/voitures/offres/bretagne/?f=a&th=1&q=Renault+Zo%C3%A9'
urlcote='http://www.lacentrale.fr/cote-auto-renault-zoe-'

# fonctions
def getContentFromUrl(url):
	r = requests.get(url)
	s = BeautifulSoup(r.text, 'html.parser')
	return s

def getLienFromUrl(url):
    s = getContentFromUrl(url);
    list_bloc=s.find("div", { "class" : "list-lbc" })
    list_article=list_bloc.findAll('a',href=True)
    list_lien=[]
    for article in list_article:
        lien=str(article['href'])
        list_lien.append(lien)
    return list_lien

def getVersionFromSoup(s):
    c=str(s.find("div", { "class" : "content" }))
    searchVersion = re.search( r'intens|life|zen', c, re.M|re.I)
    if not(searchVersion is None):
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
    km_1=s.find("div", { "class" : "lbcParams criterias" }).findAll("td")[3].string
    km=km_1.replace(" ","").replace("KM","")
    return km

def getSellerFromSoup(s):
    param=s.find("div", { "class" : "upload_by" }).find("span", { "class" : "ad_pro" })
    if param is None:
        vendeur='Particulier'
    else:
        vendeur='Professionnel'
    return vendeur

def getCoteFromVersionDate(version,date):
        no_decimal = re.compile(r'[^\d.]+')
        url_cote=urlcote+version+'+charge+rapide-'+date+'.html'
        soup=getContentFromUrl(url_cote)
        cote=soup.find("span", { "class" : "Result_Cote arial tx20" }).string
        return(no_decimal.sub('', cote))
    
result=[]

# traitement
list_liens=getLienFromUrl(url)

for lien in list_liens:
    
    s=getContentFromUrl(lien)
    titre=str(s.find("div", { "class" : "header_adview" }))    
    searchZ = re.search( r'renault|zoe|zoé', titre, re.M|re.I)
    
    if not(searchZ is None):
        
        version=getVersionFromSoup(s)
        price=getPriceFromSoup(s)
        km=getKmFromSoup(s)
        date=getDateFromSoup(s)
        seller=getSellerFromSoup(s)
        cote=getCoteFromVersionDate(version,date)
        
        for i in range(len(version)):
            if(version==version[i]):
                cote=cote[i]
                
            if price>cote:
                comparaison='oui'
            elif price<cote:
                comparaison='non'
            else:
                comparaison='égal'
                     
        resu=[version,price,km,date,seller,cote,comparaison]
        result.append(resu)
    
df = pd.DataFrame(result)
df.columns = ['version', 'prix','km','année','vendeur','cote','prix sup cote ']
print("  En Bretagne, voici la liste des voitures Renault Zoe en vente")
print(df)



    