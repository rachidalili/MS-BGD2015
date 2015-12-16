# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 20:44:18 2015

@author: Kopipan
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns
from pandas.tools.plotting import radviz, scatter_matrix
import collections
import binning









#importation des données#

path = "data/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls"
data = pd.read_excel(path,sheetname=[1,2,3,4,5,6])
df = data[2]

#supression des NaN
df = df.replace('nc',np.nan).dropna()

#extraction code Numérique
df = df[df['DEPARTEMENT'].str.contains('- ')]
df = df[df['SPECIALISTES'].str.contains('- ')]
dep = pd.DataFrame([[x] + x.split('- ') for x in df['DEPARTEMENT']],
                       columns=['DEPARTEMENT', 'num_dep', 'name_dep'])

spec = pd.DataFrame([[x] + x.split('- ') for x in df['SPECIALISTES']],
                        columns=['SPECIALISTES', 'num_spec', 'name_spec'])

df = pd.concat([df, dep, spec], axis=1, join='inner')

df['num_dep'] = df['num_dep'].str.replace('^0', '').str.replace(
        'B', '.5').str.replace('A', '.25').astype('float')

df['num_spec'] = df['num_spec'].replace('^0', '').astype('float')
df['DEPASSEMENTS (euros)'] = df['DEPASSEMENTS (euros)'].astype('float')

# ne garder que les lignes avec EFFECTIF > 0
df = df[df['EFFECTIFS'] > 0]


#Matrix 

columns = ['num_spec', 'NOMBRE DE DEPASSEMENTS','DEPASSEMENT MOYEN (euros)', 'DEPASSEMENTS (euros)', 'EFFECTIFS']
dat = df[columns]
plt.style.use('ggplot')
scatter_matrix(dat, diagonal='kde', figsize=(15,13))

#correlation entre les variables

corr_mat = dat.corr()
plt.figure(figsize=(9,9))
sns.heatmap(corr_mat, square=True, vmax=0.8)


plt.figure(figsize=(12,12))
radviz(dat, 'num_spec')


#visualisation par spécialité

groups = df.groupby(['name_spec'])
plt.figure(figsize=(12,12))
plt.title('par spé')
plt.xlabel('effectifs moyen (moyenne sur les departements)')
plt.ylabel('depassement moyen')
x = []
y = []
for name,group in groups:
    moy_eff = group['EFFECTIFS'].mean()
    moy_dep = group['DEPASSEMENT MOYEN (euros)'].mean()
    x.append(moy_eff)
    y.append(moy_dep)
    plt.plot(moy_eff, moy_dep, 'o', label=name)
    
bins = linspace(min(x),max(x),9)
count = binning_1D(bins,x,5,2,1) 
binning = binning_1D(bins,x,5,2,y)

smooth = binning/count
plt.plot(bins,smooth,'r',lw=2)


c = np.column_stack((np.asarray(x),np.asarray(y)))
data = pd.DataFrame(c, columns=['Effectifs en moyens','Depassements moyens'])

sns.jointplot('Effectifs en moyens','Depassements moyens', data=data, kind="reg", color="r", size=10)

    
#plt.legend(loc='upper right',ncol=3)
