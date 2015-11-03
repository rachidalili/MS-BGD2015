# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb

releves = [
         ['lundi','temperature',28]
         ,['lundi','ensoleillement',4]
         ,['lundi','pollution',5]
         ,['lundi','pluie',100]
         ,['mardi','temperature',28]
         ,['mardi','ensoleillement',4]
         ,['mardi','pollution',5]
         ,['mardi','pluie',100]
         ,['mercredi','temperature',28]
         ,['mercredi','ensoleillement',4]
         ,['mercredi','pollution',5]
         ,['mercredi','pluie',100]
         ,['jeudi','temperature',28]
         ,['jeudi','ensoleillement',4]
         ,['jeudi','pollution',5]
         ,['jeudi','pluie',100]
         ,['vendredi','temperature',28]
         ,['vendredi','ensoleillement',4]
         ,['vendredi','pollution',5]
         ,['vendredi','pluie',100]
         ]

cities_data = DataFrame(releves, columns=['jour','attribute','value'])
cities_data.pivot('jour','attribute','value')


aliments = pd.read_csv('aliments.csv', sep='\t')

aliments_with_traces = aliments.ix[aliments.traces.dropna().index]
traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
traces = set.union(*traces_iter)
dummies = DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns=traces)

for i, tr in enumerate(aliments_with_traces.traces):
    dummies.ix[i, tr.split(',')] = 1


pd.value_counts(pd.qcut(aliments[u'energy_100g'].dropna(),5))
pd.value_counts(pd.cut(aliments[u'energy_100g'].dropna(),5))




cameras = pd.read_csv('Camera.csv',sep=';',index_col=0)
cameras.rename(columns={'Weight (inc. batteries)':'Weight'},inplace=True)
#cameras['Max resolution'] = cameras['Max resolution'].astype(float).astype(int)
#cameras['Weight'] = cameras['Weight'].astype(float)
