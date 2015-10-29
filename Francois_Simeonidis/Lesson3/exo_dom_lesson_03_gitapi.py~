# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:21:41 2015

@author: fsimeonidis    
"""

import requests  
from bs4 import BeautifulSoup
import json

headers = {'Authorization' : 'token e15999a358e219ad8dae8097629fb9085a67b6fb'}

# fonction qui retourne le nombre moyen de stargazers des repos d'un user github
def starg_avg(user):
    url = "https://api.github.com/users/"+user+"/repos"
    response = requests.get(url, headers = headers).text
    repos = json.loads(response)
    
    stars=0
    for repo in repos:
        stars += repo['stargazers_count']
        
    return( float(stars) / len(repos) )
    
# test unitaire pour 'spicyj'
# print('unit test "spicyj" :',star_avg('spicyj'))

#%%

url = "https://gist.github.com/paulmillr/2657075"  # top contributors
request = requests.get(url, headers = headers)

soup = BeautifulSoup(request.text, 'html.parser')

# ok car 1 seule table dans la page
rows = soup.find_all('tr')
users_starg_avg = []    #  usersstarg(moyenne,userlogin)

print('GitHub 256 top contributors')

# boucle qui parcourt
for row in rows:        # 1 ligne par user
    cells = row.findChildren('td')
    if len(cells) >0:       # si th : cells null
        link = cells[0]     # le lien ok en 1ère col
        userlogin = cells[0].find('a').get_text()

        #   on crée (moyenne, user) en appelant la fonction starg_avg()
        users_starg_avg.append((starg_avg(userlogin),userlogin))
        print('-', end='', flush=True)

#  on trie et affiche users_starg_avg
users_starg_avg.sort(reverse=True)

print('>')
for res in users_starg_avg:
    print(res[1],res[0],sep='\t\t')


