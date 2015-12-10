# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 01:31:46 2015

@author: florian
"""
"""
 Récupérer via crawling la liste des 256 top contributors 
 sur cette page https://gist.github.com/paulmillr/2657075 
"""
import requests
from bs4 import BeautifulSoup
import json

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
#crawling des tops contributors
url='https://gist.github.com/paulmillr/2657075'
soup = getSoupFromUrl(url)
listContributors=[]

entries = soup.find('tbody').findAll('tr')

for entry in entries:
    listContributors.append([0,entry.find('a').get_text()])
  
#accès à l'API de GITHUB
token = '19da87b393bb22b5cc357e701875b900d0d0f717'

for i,(moyenne,contributor) in enumerate(listContributors):
    url = 'https://api.github.com/users/'+contributor+'/repos?access_token='
    request = requests.get(url+token).text
    repositories=json.loads(request)
    moyenne = 0.0
    for repo in repositories:
        moyenne += repo['stargazers_count']
    moyenne /=len(repositories)
    listContributors[i][0]=moyenne
    
listContributors.sort(reverse=True)

print([(b,a) for (a,b) in listContributors])

        
    
  
