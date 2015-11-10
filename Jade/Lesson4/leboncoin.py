# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 23:31:48 2015

@author: jade lu dac
"""

#import urllib2
from bs4 import BeautifulSoup
import requests 
import re
from  pandas import DataFrame as DF



url="http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&ps=14&q=renault+zoe"

#url2="http://www.leboncoin.fr/voitures/878729654.htm?ca=12_s"

columns=['Lieu','Année','Kilomètrage','Prix','Version','Adresse','Type annonce', 'Prix Argus','','','']
ANNONCES = DF(columns=['Lieu','Année','Kilomètrage','Prix','Version','Adresse','Type annonce', 'Prix Argus','','',''])
#url2="http://www.leboncoin.fr/voitures/715971245.htm?ca=12_s"

def getSoupFromUrl(url):
 #Execute q request toward Youtube
  request = requests.get(url)
  print (type(request))
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extract_version(description):
    # LIFE , ZEN, INTENS
    description=description.upper()
    #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    #print (description)
    if (description.rfind('LIFE') != -1):
        version= 'LIFE'
    elif (description.rfind('ZEN') != -1):
        version='ZEN'
    elif (description.rfind('INTENS') != -1):
        version='INTENS'
    else:
        version ='NON RENSEIGNEE'
    
    return(version)
      
url2="http://www.leboncoin.fr/voitures/871384960.htm?ca=12_s"   
def Get_Annonce(url2):
    soup2=getSoupFromUrl(url2)
    print(soup2)

    Pro= soup2.find("div", {"class" : "upload_by"})
    #print (Pro)

    Attrib=[]
    Donnee=[]
 

    TypeA=Pro.find("span", {"class" : "ad_pro"})
    if (TypeA!= None):
        ProV=TypeA.get_text()
    else:
        ProV="Particulier" #    print (ProV)
    Attrib.append(ProV)
    Adresse=Pro.find("a").get_text() #    print (Adresse)
    Attrib.append(Adresse)
    Prix=soup2.find("span", {"class" : "price"}).get_text() #    print (Prix)
    Prix=Prix.replace('\xa0',' ')
    Attrib.append(Prix)

    Ville=soup2.find("td", {"itemprop" : "addressLocality"}).get_text()

    CodePostal=soup2.find("td", {"itemprop" : "postalCode"}).get_text()
    Attrib.append(CodePostal+" "+Ville) #    print (CodePostal) #    print (Ville)
    descrip=soup2.find("div", {"itemprop" : "description"}) 
    #print(str(descrip))
    expr=r"0[0-9]([ .-/]?[0-9]{2}){4}"
    isphone= re.search(expr,str(descrip))
    if isphone:
        phone=isphone.group()
    else:
        phone="None"
    version=extract_version(str(descrip))
    Attrib.append(version)
    Attrib.append(phone)    
    Divsel=soup2.find("div", {"class" : "lbcParams criterias"})

    for champ in Divsel.find_all("td"):
        donnee=champ.get_text()
        donnee=donnee.replace("  ","")
        donnee=donnee.replace('\n','')
        #donnee=donnee.encode('ascii','ignore')
        #print (donnee)
        Attrib.append(donnee)
    #print (Attrib)
    #structure Attrib: 'Particulier', 'Zoé', '11 500 €', '75010 Paris', 'LIFE', 'None', 'Renault', 'Zoe', '2015', '400 KM', 'Electrique', 'Manuelle'
    #['Lieu','Année','Kilomètrage','Prix','Version','Adresse','Type annonce', 'Prix Argus']
    Donnee.append(Attrib[3])
    Donnee.append(Attrib[8])
    Donnee.append(Attrib[9])
    Donnee.append(Attrib[2])
    Donnee.append(Attrib[4])
    Donnee.append(Attrib[5])
    Donnee.append(Attrib[0])
    Donnee.append('Argus')
    return (Donnee)
    
url="http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&ps=14&q=renault+zoe"
    
    
    #return Attrib[3],Attrib[8],Attrib[9],Attrib[2],Attrib[4],Attrib[5],Attrib[0],'Argus'
#soup = BeautifulSoup(html, 'html.parser')
soup = getSoupFromUrl(url)
print(soup) 
tab_link =[]
for link in soup.find_all('a'):
    #print (type(link))
    lien=link.get('href') 
    #print (lien)
    title1=link.get('title')
    if title1 != None:
        TITLE=str(title1).lower()        
        m=re.findall('zoé',TITLE)
        #print ("trouve:"+TITLE)
        #print(m)
        if len(m) >0:
            #print ("titre: " +title1)
            tab_link.append(lien)
            print(lien)
        TITLE=str(title1).upper()        
        m=re.findall('ZOE',TITLE)
        #print ("trouve:"+TITLE)
        #print(m)
        if len(m) >0:
            #print ("titre: " +title1)
            tab_link.append(lien)
            print(lien)
           
# pour chaque offre


lesannonce=[]
for i in tab_link:
    #print (i) 
    lesannonce.append(Get_Annonce(i))

#print (lesannonce)

infos=['Lieu','Année','Kilomètrage','Prix','Version','Adresse','Type annonce', 'Prix Argus']
dff = DF(lesannonce, columns=infos) 
print (dff)


