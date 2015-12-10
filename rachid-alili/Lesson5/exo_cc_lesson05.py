# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 08:50:09 2015

@author: Kopipan
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np



lien = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
url = requests.post(lien,data={"page":1,"affNumero":0,"isAlphabet":0,"InClauseSubst":0,"typeRecherche":0,"choixRecherche":"medicament","txtCaracteres":"doliprane","radLibelle":2,"radLibelleSub":4})
soup = BeautifulSoup(url.text, 'html.parser')
result = []
for el in soup.find_all(class_="standart"):
    result.append(el.text.replace('\t','').strip())

data = pd.Series(result)

reg_string = r'(\d+,?\d*)'
reg = re.compile(reg_string)
data.str.findall(reg)




