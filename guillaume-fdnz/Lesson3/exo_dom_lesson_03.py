# coding: utf8
from __future__ import unicode_literals 
#Phase 1: Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
#Phase 2: En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users
#le nombre moyens de stars des repositories qui leur appartiennent.
#Pour finir classer ces 256 contributors par leur note moyenne.

import json
import re
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getMostActiveContributors(url):
    
  soup = getSoupFromUrl(url)
  
  tableauClassement = soup.findAll("tbody")[0]
  #Liste des liens contenant https://github.. (on évite les liens twitter et autres)
  urlContributorsPages = tableauClassement.find_all(href=re.compile("https://github.com/")) 
  # on retourne (classement, url, pseudo)
  return [ (urlContributorsPages.index(lien)+1, lien['href'], lien.text) for lien in urlContributorsPages ]

# retourne la moyenne du nombre de stars de tous les repos d'un contributeur
def getContributorAverageStarsNumber(contributorName):
    r = requests.get('https://api.github.com/users/' + contributorName + '/repos') #https://developer.github.com/v3/repos/#list-user-repositories
    if(r.ok):
        reposItems = json.loads(r.text or r.content)
        return sum([repo['stargazers_count'] for repo in reposItems]) / float(len(reposItems))

# retourne le classement des top contributeurs par ordre décroissant de nombre moyen de stars/repo
def getContributorsStarsRanking(mostActiveContributors):

    averageStarsByContributor = [(getContributorAverageStarsNumber(pseudo),pseudo) for (classement, url, pseudo) in mostActiveContributors]
    averageStarsByContributor.sort(key=lambda contributor: contributor[0], reverse=True) # + grand nombre de stars en premier   
    return averageStarsByContributor

def displayBeautifulData(mostStargazedContributors):
    print '| Classement des top contributeurs ayant la plus grande moyenne de stars'
    for (averageStars,pseudo) in mostStargazedContributors:
        print '| ',round(averageStars,2), ' | ',pseudo
        print "--------------------------------"
    

url = "https://gist.github.com/paulmillr/2657075"
mostActiveContributors = getMostActiveContributors(url)
mostStargazedContributors = getContributorsStarsRanking(mostActiveContributors)

displayBeautifulData(mostStargazedContributors)
