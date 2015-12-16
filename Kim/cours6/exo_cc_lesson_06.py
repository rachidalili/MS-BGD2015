# -*- coding: utf-8 -*-
"""
@author: kim
"""


import re
import pandas as pd

data = pd.read_excel('data_cours6/exo.xls', sheet_name='INPUT > Merlin Summary', header=11, skip_rows=11, index_col=None)

#deux methodes possibles pour construire une colonne avec partie du texte des valeurs d une autre colonne
data['site'] = list(map(lambda x: re.split(' | ', x)[0] , list(data['article_title'].astype(str))))
#data['site'] = data['article_title'].str.split(' | ').str[0] #recup str avant le |
data['country'] = data['campaign'].str.split('_').str[1] #recup deuxieme str apres le _
data['target'] = data['campaign'].str.split('_').str[2] #recup troisieme str apres le _

#aggregation, affiche les moyennes des colonnes impressions et revenue en fonction dans l'ordre de site de vnte, ays, type mkting et cible, met un zero si pas de valeur
pivot = pd.pivot_table(data, ['revenue', 'impressions'], index=['site', 'country', 'viral', 'target'], aggfunc='mean', fill_value=0)

print pivot
