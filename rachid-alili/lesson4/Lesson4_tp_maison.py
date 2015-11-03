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



