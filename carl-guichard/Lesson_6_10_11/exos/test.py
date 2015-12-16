import pandas as pandas
import numpy as numpy

data_page1 = pandas.read_excel('/Users/Carl/Documents/MyDocuments/Universites/Cours/Telecom_paristech/Git/MS-BGD2015/MS-BGD2015/carl-guichard/Lesson_6_10_11/exo.xls', skiprows = 11, sheetname = 0)
data_page2 = pandas.read_excel('/Users/Carl/Documents/MyDocuments/Universites/Cours/Telecom_paristech/Git/MS-BGD2015/MS-BGD2015/carl-guichard/Lesson_6_10_11/exo.xls', skiprows = 11, sheetname = 1)

print (data_page1.head())
#print data_page1.columns
#print data_page2.columns

# on veut recuperer Les pays, sites, target, Vicel sponsored
# on veut le total impressions revenus pour chaque groupe 

data_page1[['country']] = df['campaign'].str.split('_').str[1]
data_page1[['target']] = df['campaign'].str.split('_').str[3]

res = data_page1.groupby(['country', 'target'])[['impressions', 'revenue']].mean()