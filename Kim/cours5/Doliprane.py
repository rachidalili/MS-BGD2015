__author__ = 'kim'


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



def fromUrltoSoup( url):
    r = requests.get(url,  stream=True)
    return BeautifulSoup(r.text, 'html.parser')

url = u'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

#je recupere params avec la requete post envoyee quand je recherche doliprana

params = {'txtCaracteres': 'dolipra', 'choixRecherche':'medicament'}

r = requests.post(url, data=params)

soup = BeautifulSoup(r.text)

balises =  soup.find_all(class_ = "standart")

names = [x.text for x in balises]

#print names

names = pd.Series(names)
names = names.str.strip()

print names

reg_string = r'(\d+,?\d*) (\w+), ((\w|\s)+)'

reg = re.compile(reg_string)

names.str.findall(reg)

print names