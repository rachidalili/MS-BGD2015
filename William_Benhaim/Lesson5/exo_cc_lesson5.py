import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def FromTestToInt(txt):
    return int(txt.replace(u'\xa0', u'').replace(u'\u20ac', u'').replace(' ', ''))


def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def recupKM(txt):
    return int(txt.replace(u'KM', u'').replace(u'\nKilom\xe9trage :', u'').replace(' ', ''))


def coteLacentrale(modele, annee):
    url_cote = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + \
        modele + '+charge+rapide-' + annee + '.html'
    soupCoteArgus = GetSoupFromUrl(url_cote)
    Cote = soupCoteArgus.find('span', {'class': 'Result_Cote arial tx20'})
    return FromTestToInt(Cote.text)


url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
param = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0, 'inClauseSubst': 0, 'nomSubstances': '', 'typeRecherche': 0, 'choixRecherche': 'medicament',
         'txtCaracteres': 'doliprane', 'btnMedic.x': 13, 'btnMedic.y': 11, 'btnMedic': 'Rechercher', 'radLibelle': 1, 'txtCaracteresSub': '', 'radLibelleSub': 4}
request = requests.post(url, data=param)
soup = BeautifulSoup(request.text, 'html.parser')
med = soup.findAll('a', {'class': 'standart'})
# for x in med:
# 	print x.text
names = [x.text for x in med]
# 
# print names
