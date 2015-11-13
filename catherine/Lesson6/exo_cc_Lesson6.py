# -*- coding: utf-8 -*-
__author__ = 'catherine'

import pandas as pd

def getCampain():
    df = pd.read_excel("exo.xls", sheetname=0, skiprows=11)
    return df

print(pd.__version__)
df = getCampain()

r1 = df['campaign'].str.split('_').str[1:3]
df[['country', 'target']] = df['campaign'].str.extract('_([A-Z]{2})_([\w\s]*)')
res = df.groupby(['country'])[['impressions', 'revenue']].mean()
print(res)
res = df.groupby(['country', 'target'])[['impressions', 'revenue']].mean()
print(res)