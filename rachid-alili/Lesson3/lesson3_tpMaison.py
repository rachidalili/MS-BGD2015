########################################################
# imports 
########################################################

import requests as re
# import re 
from bs4 import BeautifulSoup
import json
import pandas as pd
from getpass import getpass


# pour afficher de jolis tableaux
import tabulate


########################################################
# fonctions communes 
########################################################
#Return soup from url
def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup



########################################################
# fonctions du projet 
########################################################

#recupere  username, password - limitation de gitup
def auth() :
	username = input('GitHub username:')
	password = getpass()
	return username,password

#Return score from contributeur name
def getScore(contrib,username,password):
	star_nb =0.0
	project_nb=0.0
	user_url = "https://api.github.com/users/" + contrib + "/repos"
	json = requests.get(url=user_url, auth=(username,password)).json()
	for project in json:
			star_nb += project['stargazers_count']
			project_nb += 1
	return star_nb/project_nb

#Return all datas in a sorted panda dataframe
def getData():
	df = pd.DataFrame(columns=['contrib', 'nb_star'])
	username, password = auth()
	url = 'https://gist.github.com/paulmillr/2657075'
	soup = getSoupFromUrl(url)
	line = 0
	for contrib in soup.select("tr > td:nth-of-type(1) > a"):
		score = getScore(contrib.text, username, password)
		print(str(line) + " " + contrib.text + " " + str(score))
		#Add in panda dataframe
		df = df.append(pd.Series({'contrib':contrib.text,'nb_star':score}, index=['contrib', 'nb_star']), ignore_index=True)
		line += 1
	#sort panda dataframe
	sorted_list = df.sort('nb_star', ascending=False)
	return(sorted_list)

#show dataframe with style
def prettyPrint(sorted_list):
	print(tabulate(sorted_list, headers=['contrib', 'nb_star'], tablefmt='psql'))


#####################################################""
# code execution
datas = getData()
prettyPrint(datas)
