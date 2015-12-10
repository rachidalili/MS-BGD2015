# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:31:27 2015

@author: yop
"""

import pandas as pd

File = "./data/exo.xls"
df = pd.read_excel(File, sheetname = "INPUT > CM Tool", skiprows=range(11))
df = pd.DataFrame(df)

df[["country", "target"]] = df['campaign'].str.split("_").str[1:3]

print(df.groupby('country')[['IMPRESSIONS','revenue']].mean)
#group_Geo = df.groupby('Geo')

#for el in group_Geo:
#    meanImpr = df["IMPRESSIONS"].mean()
#    print(el , meanImpr)



#print(df.head())

