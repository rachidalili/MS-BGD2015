# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 08:37:33 2015

@author: jeanlucla
"""
import requests
from bs4 import BeautifulSoup
from github import Github


# ############    Scraping  ###################

url = "https://gist.github.com/paulmillr/2657075"
data = []
users_list = []
count = 0

# on charge le contenur de l'url dans Soup
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')


# on recherche toutes les data dans la page qui corespondent a
# l'arborescence :
#  <article>
#  - <table>
#     - <tr>
data = soup.find('article').find('table').findAll('tr')

# pour chaque data correspond un user
for user in data:
    # teste la première ligne (evite d'être bloqué par le header)
    if user.find('th').get_text() != "#":
        # recupère le pseudo du user
        pseudo = user.find('td').find('a').get_text()
        # nettoie l'encodage et enlève les 'u'
        pseudo = pseudo.encode('utf-8').strip()
        users_list.append(pseudo)


print users_list
print len(users_list)


# ####################   API Github  #######################

stargazers_count = 0
stargazers_avg = 0
final_list = []

# Lecture du Token généré par GitHub
Access_Token = open('/Users/jeanlucla/workspace/charles/AccessToken.txt', 'r').read()
print Access_Token

# pour chaque user dans la liste
for i in range(len(users_list)):
    # print users_list[i]
    # on recupère de login / pwd du user
    g = Github(users_list[i], password[i])
    repos = g.get_user().get_repos()
    # on compte le  nombre de stars pour chacun des repo du user
    for repo in repos:
        # print repo.full_name
        print repo.stargazers_count
        stargazers_count = stargazers_count + repo.stargazers_count
    # moyenne du nombre de stargazer nb de stargazers-/ par le nb de repos
    stargazers_avg = stargazers_avg / len(repos)
    # ajout du nom et de la moyenne des stars dans la table finale
    final_list.append(users_list[i], stargazers_avg)
    # print stargazers_avg

# Tri de la liste finale par nb de stargazers moyens décroissant

print sorted(final_list, key=final_list[1], reverse=True)
