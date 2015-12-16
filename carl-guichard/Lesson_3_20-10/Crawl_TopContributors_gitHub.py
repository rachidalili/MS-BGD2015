#-*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:34:20 2015

@author: Carl
"""

#
# Exercice 1 :
# Recuperer via crawling la liste des 256 top contributors sur cette page
#  https://gist.github.com/paulmillr/2657075
#

#
# Exercice 2 :
#Crawler avec l'API pour recuperer le nombre d'étoile  de chaque ...
#...repository qui appartient aux différents top utilisateur. Puis faire une moyenne de ces étoiles et classer par ordre.
#

import requests
from bs4 import BeautifulSoup
import json
import numpy as np

""" return the soup from a web link """
def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup



def getTop256Accounts(soup):
    """
    return the list composed of top 256 git used and their webpage link.
    The mothod employed here is a simple soup crawling
    """
    links_users = {}
    tags = soup.find_all(lambda tag: tag.name == 'a' \
                        and tag.parent.name == 'td' \
                        and tag.attrs['href'].find("https://github.com") != -1)
    for tag in tags:
        links_users.update({tag.get('href') : tag.text})
    return links_users



def getAuthFromFile(file_name = 'secret.txt'):
    """
    return the token and username from a file.
    """
    f = open(file_name, 'r')
    lines = f.readlines()
    username = lines[0]
    password = lines[1]
    return username, password



def checkAuth(username, password):
    """
    Check connection with id and pass
    """
    r = requests.get('https://api.github.com/user', auth=(username, password))
    return r.status_code == 200



def authentification():
    """
    Since this script requires more than 60 API request / hours,
    we need to authentificate as a GitHub user.
    Returns:
    --------
    tuple (username, password)
    """
    username, password = getAuthFromFile()
    if checkAuth(username, password):
        return (username, password)
    else:
        print ("Erreur d'identification")



def getUserAverageStars(user, auth):
    """
    For one user return its average star number
    """
    url = 'https://api.github.com/users/' + user + '/repos'
    r = requests.get(url=url, auth=auth)
    answer = json.loads(r.text)
    stargazers_count = []
    for line in answer:
        if line['stargazers_count']:
            stargazers_count.append(line['stargazers_count'])
    return np.mean(stargazers_count)



""" return the list composed with the users and the average star scoring """
def getUsersAverageStars(links_users, auth):
    users_stars = []
    for user in links_users.values():
        star_number = getUserAverageStars(user, auth)
        users_stars.append([star_number, user])
    return users_stars



def writeAnswerInFile(users_stars):
    """
    copy the results in a file
    """
    f = open('answer.txt', 'w')
    for item in sorted(users_stars, reverse=True):
        f.write("%s\n" % item)



url = "https://gist.github.com/paulmillr/2657075"
soup = getSoupFromUrl(url)
links_users = getTop256Accounts(soup)
auth = authentification()
users_stars = getUsersAverageStars(links_users, auth)
writeAnswerInFile(users_stars)
print sorted(users_stars, reverse=True)















