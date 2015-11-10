# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt
from numpy.random import randn
#import statsmodels.api as sm


time = '08-10-1998'
datetime.strptime(time, '%d-%m-%Y')

nursing = pd.read_csv('Nursing_data_11_29_2012.csv', sep='\t')
nursing = nursing.set_index('Date')
nursing.index = nursing.index.map(lambda x : parse(x))

wiki_data  = pd.read_csv('smallwikipedia.csv', sep=';')
wiki_data = wiki_data.drop(0)
wiki_data = wiki_data.set_index('Date')
wiki_data.index = wiki_data.index.map(lambda x : parse(x))
wiki_data['changes'] = wiki_data['changes'].astype(int)



death_data = pd.read_csv('CausesOfDeath_France_2001-2008.csv')
death_data['Value'] = death_data['Value'].str.replace(' ','')
death_data['Value'] = death_data['Value'].apply(lambda x : int(re.compile(r'[^0-9]').sub('0',x)))
death_data = death_data[['ICD10','Value','SEX','TIME']]

causes = death_data.groupby('ICD10')['Value'].sum().order(ascending=False)[0:5].index.values

filtered = death_data[death_data['ICD10'].isin(causes)]

filtered_agg = filtered.groupby(['ICD10','TIME']).sum()

filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot()
filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="bar")
filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="barh")
filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="barh", stacked=True)

cars = pd.read_csv('cars.csv',sep=';',index_col=0).drop('STRING')
cars['MPG'] = cars['MPG'].astype(float)
cars['Cylinders'] = cars['Cylinders'].astype(float)
cars['Weight'] = cars['Weight'].astype(float)
cars['Acceleration'] = cars['Acceleration'].astype(float)
cars['Horsepower'] = cars['Horsepower'].astype(float)
pd.scatter_matrix(cars, diagonal='kde', color='k', alpha=0.3)

