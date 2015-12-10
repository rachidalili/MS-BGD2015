# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:53:54 2015

@author: Kopipan
"""

import pandas as pd
import time




debut = time.time()
dataset = pd.read_excel("C:\Users\Kopipan\MS-BGD2015\Lessons-Exercices\exo.xls",sheetname='INPUT > Merlin Summary', skip_rows=11,header=11)

dataset['country'] = dataset['campaign'].str.split('_').str[1]

dataset['target'] = dataset['campaign'].str.split('_').str[2]

groups_target_country = dataset.groupby(['country','target'])[['impressions','revenue']].mean()

print groups_target_country
fin = time.time()

duree = fin - debut
print(duree)

