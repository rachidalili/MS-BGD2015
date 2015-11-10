import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_excel("../../Lessons-Exercices/exo.xls", skiprows=11, sheetname=0)
print(df.head())


country = pd.DataFrame([x.split('_')[1:3] for x in df['campaign']],
                       columns=['country', 'target'])

print(country)

df = pd.concat([df, country], axis=1, join='inner')

groups_country = df.groupby('country')

print('country, target,    revenue ,      impression  ')

for country, group in groups_country:

    group_target = group.groupby('target')
    for target, group2 in group_target:
        # print(country, target)
        print("%4a % 15a: % 10.3f  % 10.3f" %
              (country, target, group2['revenue'].mean(), group2['impressions'].mean()))

    # corr = group[['Clics', 'likes', 'shares', 'comments', 'revenue']].corr()
    # print(name)
    # print(corr)
