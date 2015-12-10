 
###Package Importation#########

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import re
import json

###############################


#####Functions#################

def loadpage(MyPage):
	page = requests.get(MyPage)
	soup = BeautifulSoup(page.text,'html.parser')
	return soup

def GetInfos(link="http://www.leboncoin.fr/voitures/872265494.htm?ca=12_s"):
    lbc_soup = loadpage(link)
    infos = lbc_soup.findAll("div", {"class": "lbcParams criterias"})
    return infos

def getparams(params,itemprop):
    return params[0].find_all("td", {"itemprop":itemprop})

def get_km(params):
    table_of_tds = params[0].find_all('td')
    for td in table_of_tds:
        m = re.match(".*(KM).*", td.text, re.IGNORECASE)
        if m:
            return int(td.text.replace(m.group(1), '').replace(' ',''))

def get_pro_or_not(link='http://www.leboncoin.fr/voitures/872265494.htm?ca=12_s'):
    leBonCoin_soup = loadpage(link)
    uploaded_by = leBonCoin_soup.find_all("div", {"class":"upload_by"})
    pro_address = uploaded_by[0].find_all("span", {"class":"ad_pro"})
    return "professional" if len(pro_address) == 1 else "individual"
    
params = GetInfos()
comparison = []
year = getparams(params, "releaseDate")[0].text.replace(' ', '').strip()
km = get_km(params)
uploader = get_pro_or_not()

comparison.append([year, km, uploader])
print comparison

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


def getads(search="renault zoe"):
    idf = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q='+ search.replace(' ','+')
    paca = 'http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?q='+ search.replace(' ','+')
    aquitaine = 'http://www.leboncoin.fr/voitures/offres/aquitaine/?q='+ search.replace(' ','+')
    
    regions = [idf,paca,aquitaine]
    ads = []
    for region in regions:
        offers = loadpage(region).find_all("div",{'class':'list-lbc'})[0]
        ads_for_region = offers.find_all('a')
        for ad in ads_for_region:
            ads.append(ad['href'])
    
    return ads

matrix = []
all_ads = getads()
for ad in all_ads:
    matrix.append(get_data_from_page(ad))
print matrix



#creation tableau

columns = ['Version', 'Year', 'Km', 'Price', 'Posted by', 'Phone']
datacars = pd.DataFrame(matrix, columns = columns)

def get_argus_from_car(car):
    version = car[['Version']].item()
    year = car[['Year']].item()

    if version != '':
        argus_page = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'+version+'+charge+rapide-'+year+'.html'
        res = loadpage(argus_page)
        argus_with_currency = res.find_all('span', {'class':'Result_Cote arial tx20'})[0].text.replace(' ', '')
        matches = re.match('([0-9]*)', argus_with_currency)
        argus = matches.group(1)
        return argus
    else:
        return "0"

argus_list = []
for i in range(0,datacars.shape[0]):
    argus_list.append(get_argus_from_car(datacars.irow(i)))

argus_list_ = pd.DataFrame(argus_list, columns=['Argus'])

datacars_with_argus = pd.concat([datacars, argus_list_], axis=1)
datacars_with_argus['Phone'][0] = datacars_with_argus['Phone'][0].replace('.','').replace('R','')

datacars_with_argus[['Year', 'Km', 'Price', 'Argus']] = datacars_with_argus[['Year', 'Km', 'Price', 'Argus']].astype(int)
datacars_with_argus.dtypes

def compare(price,argus):
    if price.item() <= argus.item():
        return "cheap"
    else:
        return "expensive"

aa = datacars_with_argus.apply(lambda row: compare(row[['Price']], row[['Argus']]), axis=1)
datacars_with_argus['Evaluation'] = datacars_with_argus.apply(lambda row: compare(row[['Price']], row[['Argus']]), axis=1)

datacars_with_argus.to_csv("cars.csv", sep=';')

    

