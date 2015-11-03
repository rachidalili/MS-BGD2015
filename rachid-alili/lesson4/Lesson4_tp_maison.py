###Package Importation#########

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import re
import json

###############################


#chercher les parametres
my_soup = loadpage("http://www.leboncoin.fr/voitures/848861858.htm?ca=12_s"  )
params = my_soup.findAll("div", {"class": "lbcParams criterias"})
 

tab_comparaison = []
# year = getparams(params, "releaseDate")[0].text.replace(' ', '').strip()

#"recuperer l'annee"
year = params[0].find_all("td", {"itemprop":"releaseDate"})
year = year[0].text.replace(' ', '')
year = year.strip()


#"recuperer  kilometrage"

table_td = params[0].find_all('td')

for td in table_td:
    #regex
    m = re.match(".*(KM).*", td.text, re.IGNORECASE)
    if m:
        kilometrage = td.text.replace(m.group(1), '')
        kilometrage = int(kilometrage.replace(' ',''))

# "verifier si pro"
 
uploader = my_soup.find_all("div", {"class":"upload_by"})
adr_pro = uploader[0].find_all("span", {"class":"ad_pro"})
uploader = "professionel" if len(adr_pro) == 1 else "particulier"

tab_comparaison.append([year, kilometrage, uploader])
#print tab_comparaison



##############################

def get_info_as_json(link):
    leBonCoin_soup = loadpage(link)
    js = leBonCoin_soup.find_all("script", {"type":"text/javascript"})[2].text
    js = js.replace("\nvar utag_data = ",'').replace('\n','')
    js = js.replace(' ','').replace('"','')
    js = js.replace(':',"\":\"").replace(',',"\",\"")
    js = js.replace('{',"{\"").replace('}',"\"}")
    #m = re.match("(.*\n*)*pagetype : \"([^\"]+)\".*", json)
    #print js
    return json.loads(js)


def get_version_from_title(title):
    m = re.match(".*(intens|zen|life).*", title, re.IGNORECASE)
    if m and len(m.groups()) >= 1:
        return m.group(1)
    else:
        return ""

def get_phone_number(link='http://www.leboncoin.fr/voitures/872265494.htm?ca=12_s'):
    mySoup = loadpage(link)
    b = mySoup.select('div[class="AdviewContent"] > div[class="content"]')
    description = b[0].text.replace('\n','').strip()
    
    m = re.search("^.*\D?(0[0-9].?([0-9][0-9].?){4})\D?.*$", description)
    if m and len(m.groups()) >= 1:
        return m.group(1)
    return None

def get_data_from_page(link='http://www.leboncoin.fr/voitures/872265494.htm?ca=12_s'):
    myJson = get_info_as_json(link)
    version = get_version_from_title(myJson["titre"]).lower()
    return (version,
            myJson["annee"], 
            myJson["km"], 
            myJson["prix"], 
            myJson["offres"], 
            get_phone_number(link))


# chercher tous les vehicules renault zoe des trois regions

liste_vehicules = []
search="renault zoe"
idf = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q='+ search.replace(' ','+')
paca = 'http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?q='+ search.replace(' ','+')
aquitaine = 'http://www.leboncoin.fr/voitures/offres/aquitaine/?q='+ search.replace(' ','+')

regions = [idf,paca,aquitaine]
offres = []
for region in regions:
    offres_region = loadpage(region).find_all("div",{'class':'list-lbc'})[0]
    items_region = offres_region.find_all('a')
    for item in items_region:
        offres.append(item['href'])
    

for item in offres:
   liste_vehicules.append(get_data_from_page(item))
print liste_vehicules

