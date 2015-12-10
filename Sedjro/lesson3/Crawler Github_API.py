# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:23:46 2015

@author: bibiane
"""

import requests
from bs4 import BeautifulSoup
import json
import urllib2
import re
from getpass import getpass

def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')
    

soup = GetSoupFromUrl('https://gist.github.com/paulmillr/2657075')

"""En inspectant l'élément , on se rend compte que le nom que nous cherchons est situé
dans une balise td située dans une balise tr"""
allbigContribs = soup.findAll("tr", {"td": ""})

"""Une fois sortie tous les types de résultats de cette forme, on se rend compte,
qu'il y a plusieurs balises td dans notre balise tr, dès lors il faut qu'on lui
énumère laquelle des balises nous intéresse et dans ce cas précis on peut se rendre
compte que c'est la première balise td , d'où le td:nth-of-type(1) """

allbigContribs2 = soup.select('tr > td:nth-of-type(1) > a')

red=allbigContribs2.findAll("a")

""" """
def auth() :
	username = raw_input('GitHub username:')
	password = getpass()
	return username,password

username, password = auth()

"""  """
def getScore(contrib,username,password):
	star_nb =0.0
	project_nb=0.0
	user_url = "https://api.github.com/users/" + contrib + "/repos"
	json = requests.get(url=user_url, auth=(username,password)).json()
	for project in json:
			star_nb += project['stargazers_count']
			project_nb += 1
	return star_nb/project_nb






ssedjro, francis89 = auth()

Liste_names = []

for bc in allbigContribs:
    #bigContrib = bc.findAll("a")
    # print bc
    bigContrib = bc.select('td:nth-of-type(1) > a')
    
    """ Si je run le bigContrib, il choisit le dernier élement de la liste 
    des bigContrib et me sort tout ce qui se trouve dans la balise <a> """
    
    for el in bigContrib:
        Liste_names.append({'util': el.text}) 
        
    """ Pour tout élément appartenant au bigContrib, je prends juste le tecte
    qu'il contient """
    """ Ce texte je l'implémente dans ma Liste_names que j'ai initialisé au
    préalable, je rajoute le préfixe util"""
    """ Si je run toute ma boucle, il me sors tous mes résultats """
    
    for nbLS in range(len(Liste_names)):
        urlApi = 'https://api.github.com/users/' + \
        Liste_names[nbLS]['util'] + '/repos'
    # rajouter le mot de passe. a ameliorer
        resp = requests.get(url=urlApi, auth=(username, password))
        data = json.loads(resp.text)
        sommestargazers = 0.0