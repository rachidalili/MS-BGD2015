# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:27:22 2015

@author: Kopipan
"""
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





