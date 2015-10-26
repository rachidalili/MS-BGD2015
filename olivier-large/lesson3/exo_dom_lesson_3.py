import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
from getpass import getpass
from tabulate import tabulate

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def auth() :
	#to pass request limitation
	username = input('GitHub username:')
	password = getpass()
	return username,password

def getData():
	df = pd.DataFrame(columns=['contrib', 'nb_star'])
	all_data=[]
	username, password = auth()
	url = 'https://gist.github.com/paulmillr/2657075'
	soup = getSoupFromUrl(url)
	line = 1
	for contrib in soup.select("tr > td:nth-of-type(1) > a"):
		user_url = "https://api.github.com/users/" + contrib.text + "/repos"
		json = requests.get(url=user_url, auth=(username,password)).json()
		star_nb =0.0
		project_nb=0.0
		for project in json:
			star_nb += project['stargazers_count']
			project_nb += 1
		print(str(line) + " " + contrib.text + " " + str(star_nb/project_nb))
		line +=1
		df = df.append(pd.Series({'contrib':contrib.text,'nb_star':star_nb/project_nb}, index=['contrib', 'nb_star']), ignore_index=True)
	sorted_list = df.sort('nb_star', ascending=False)
	return(sorted_list)

def prettyPrint(sorted_list):
	print(tabulate(sorted_list, headers=['contrib', 'nb_star'], tablefmt='psql'))

datas = getData()
prettyPrint(datas)
