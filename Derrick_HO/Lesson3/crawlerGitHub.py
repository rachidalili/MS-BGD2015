# coding: utf8

import requests
import json
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import operator

URL = 'https://gist.github.com/paulmillr/2657075'
# GIT_LOGIN ############ Complete
# GIT_PWD ############ Complete
# GIT_TOKEN 

def getSoupFromUrl(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def getUsers(url):
	soup = getSoupFromUrl(url)
	usersList = []

	blocs = soup.find_all('article', {'class': 'markdown-body entry-content'})
	table = soup.find('table')
	rows = table.find_all('tr')
	for row in rows:
		cell = row.find_all('td')	
		if cell:
			href = cell[0].find_all('a', href=True)
			name = href[0].text
			# link = href[0]['href']
			# usersList[name] =  link
			usersList.append(name)
	return usersList

# Authentification github par id/mdp
def requestGithubAPI(user):
	request = requests.get('https://api.github.com/users/' + user + '/repos', auth=(GIT_LOGIN, GIT_PWD))
	return request

# Authentification gitHub par Token
def authGihubAPI(user):
	url = 'https://api.github.com/users/' + user + '/repos'
	headers = {'Authorization': 'token %s' % GIT_TOKEN}
	r = requests.get(url, headers=headers)
	return r

def getMean(jsonText):
	sum = 0
	for attributes in jsonText:
		sum+=attributes['stargazers_count']
	mean = float(sum)/ float(len(jsonText))
	return mean

def main():
	users = getUsers(URL)
	usersDict = {}
	for name in users:
		# r = requestGithubAPI(name)
		r = authGihubAPI(name)
		jsonText = json.loads(r.text)
		mean = getMean(jsonText)

		if name not in usersDict:
			usersDict[name] = mean
			
	usersDictSorted = sorted(usersDict.items(), key=operator.itemgetter(1))
	pdDict = pd.DataFrame(usersDictSorted)
	print pdDict

if __name__ == '__main__':
	main()