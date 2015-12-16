# coding: utf-8

import pandas as pd

data = pd.read_excel('/Users/jeremieguez/Documents/MS-BGD2015/Lessons-Exercices/exo.xls', sheet_name='INPUT > Merlin Summary', header=11, skip_rows=11, index_col=None)
data['site'] = data['article_title'].str.split(' | ').str[0]
data['country'] = data['campaign'].str.split('_').str[1]
data['target'] = data['campaign'].str.split('_').str[2]

pivot = pd.pivot_table(data, ['revenue', 'impressions'], index=['site', 'country', 'viral', 'target'], aggfunc='mean', fill_value=0)

print (pivot)
