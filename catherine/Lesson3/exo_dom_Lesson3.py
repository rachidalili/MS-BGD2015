__author__ = 'catherine'

#
# Devoir maison Lesson 3 : crawling + Restful API sur GitHub
#

github_api_url = "https://api.github.com"
my_token = ""

import requests
from bs4 import BeautifulSoup
import json
import unittest


#
# Exercice 1 :
# Récupérer via crawling la liste des 256 top contributors sur cette page
#  https://gist.github.com/paulmillr/2657075
#

#
# Récupérer le parsing Soup d'une page HTML accessible via le paramètre url
#
def getSoupFromUrl(url):
    #Execute q request toward Youtube
    request = requests.get(url)
    #parse the restult of the request
    soup = BeautifulSoup(request.text, 'html.parser')
    request.connection.close()
    return soup

#
# récupérer les 256 Top contributeurs sur la page
# on filtre sur les tags 'a' dans une cellule de tableau dont l'attribut href contient
# la chaîne 'https://github.com'
#
def getTop256Accounts(soup):
    tags = soup.find_all(lambda tag: tag.name == 'a' \
                        and tag.parent.name == 'td' \
                        and tag.attrs['href'].find("https://github.com") != -1)
    return tags

#
# Exercice 2 : récupérer pour chacun de ces users le nombre moyens de stars des
#  repositories qui leur appartiennent
#

rqHeader = {"Authorization": "token "+my_token}
#
# Connect to github api using token
#
def connectWithToken():
    request = requests.get(github_api_url+"/user", headers=rqHeader)
    return request.status_code

#
# Retrieve repositories for a given user with the tag got for exercice 1
#
def getUserRepositoriesFromTagUser(tag_user):
    user_name = tag_user.contents[0]
    request = requests.get(github_api_url+"/users/"+user_name+"/repos?type=owner", headers=rqHeader)
    if request.status_code == 200:
        return json.loads(request.text)
    else:
        return None

#
# Stars mean for all repositories
#
def getUserRepositoriesStarMean(tag_user):
    repos = getUserRepositoriesFromTagUser(tag_user)
    stars = 0
    if repos is not None:
        for repo in repos:
            stars += repo['stargazers_count']
        return stars/len(repos)
    else:
        return stars

soup = getSoupFromUrl("https://gist.github.com/paulmillr/2657075")
tags = getTop256Accounts(soup)
print(len(tags))
"""
i = 1
for tag in tags:
    print(i, tag)
    i += 1
"""
result = {}
connect_status = connectWithToken()
if connect_status == 200:
    for tag in tags:
        print(tag)
        star_mean = getUserRepositoriesStarMean(tag)
        result[tag.contents[0]] = star_mean

for entry in result.keys():
    print(entry + "  ==>  "+str(result[entry]))