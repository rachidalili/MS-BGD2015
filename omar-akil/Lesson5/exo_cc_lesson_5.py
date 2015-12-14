"""
@author: omakil
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

lien = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
df = pd.DataFrame(columns=['Medicament', 'Dosage', 'Unite','Remarque', 'Type'])

for page in range(1, 3):
    print 'page ' + str(page)
    r = requests.post(lien, {
        "page": page,
        "affliste": 0,
        "affNumero": 0,
        "isAlphabet": 0,
        "inClauseSubst": 0,
        "nomSubstances": '',
        "typeRecherche": 0,
        "choixRecherche": 'medicament',
        "txtCaracteres": 'doliprane',
        "btnMedic.x": '12',
        "btnMedic.y": '5',
        "btnMedic": 'Rechercher',
        "radLibelle": 2,
        "txtCaracteresSub": '',
        "radLibelleSub": 4
    })
    s = BeautifulSoup(r.text, 'html.parser')
    liens = s.findAll('a', {'class': 'standart'})
    for l in liens:
        text = l.get_text()
        tokens = re.findall(r'(.*)\s(\d{2,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)', text)      
        if len(tokens) > 0 :
            df = df.append({
                'Medicament': (tokens[0][0] + ' ' + tokens[0][3]).strip(),
                'Dosage': int(tokens[0][1]),
                'Unite': tokens[0][2],
                'Remarque': tokens[0][3],
                'Type': tokens[0][4].strip()
            }, ignore_index=True)


print df
