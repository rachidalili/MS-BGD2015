__author__ = 'catherine'

#
# Devoir maison Lesson 3 : crawling + Restful API sur GitHub
#

github_api_url = "https://api.github.com"

import requests
from bs4 import BeautifulSoup
import json


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

#
# Connect to github api using token
#
def connectWithToken(rqHeader):
    request = requests.get(github_api_url+"/user", headers=rqHeader)
    return request.status_code

#
# Retrieve repositories for a given user with the tag got for exercice 1
# Autorization key should be added because the number of requests exceeds 60
#
def getUserRepositoriesFromTagUser(tag_user, rqHeader):
    user_name = tag_user.contents[0]
    request = requests.get(github_api_url+"/users/"+user_name+"/repos?type=owner", headers=rqHeader)
    if request.status_code == 200:
        return json.loads(request.text)
    else:
        return None

#
# Stars mean for all repositories
#
def getUserRepositoriesStarMean(tag_user, rqHeader):
    repos = getUserRepositoriesFromTagUser(tag_user, rqHeader)
    stars = 0
    if repos is not None:
        for repo in repos:
            stars += repo['stargazers_count']
        return stars/len(repos)
    else:
        return stars

print("Enter a github token to get Top256 contributors:")
my_token = input(">>>")
rqHeader = {"Authorization": "token "+my_token}
soup = getSoupFromUrl("https://gist.github.com/paulmillr/2657075")
tags = getTop256Accounts(soup)
#print(len(tags))

result = []
connect_status = connectWithToken(rqHeader)

if connect_status == 200:
    i = 1
    for tag in tags:
        print("processing "+ str(i)+" "+str(tag))
        star_mean = getUserRepositoriesStarMean(tag, rqHeader)
        result.append([tag.contents[0], star_mean])
        i += 1
    # sort result
    result = sorted(result, key=lambda contributor: contributor[1], reverse=True)
    for entry in result:
        print(entry[0] + "  ==>  "+str(entry[1]))
else:
    print("Unable to connect / check your token")

