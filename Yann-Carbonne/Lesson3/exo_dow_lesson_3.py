#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import urllib2, base64
import json
import operator
import sys

# ============= README =============
# 
# Do NOT use regular expressions to parse HTML at home
# -> http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454
#
# ============ /README =============
# ============= TODO =============
# 
# add Threads
#
# ============ /TODO =============


# CONFIGURATION
URL_GIT_USERS = 'https://gist.github.com/paulmillr/2657075'
URL_GIT_API_REPOS_BY_USER = 'https://api.github.com/users/%USER%/repos'
GIT_LOGIN = 'lahw'
# Get your token there : https://github.com/settings/tokens/new
AUTH_KEY = '4a260594ba63108e7c86f74e41a22a962b80903a'
NB_USERS = 10


# ============= FUNCTIONS =============
def getJson (user):
	"""Get the JSON in text for a given user."""
	request = urllib2.Request(URL_GIT_API_REPOS_BY_USER.replace('%USER%', user))
	base64string = base64.encodestring('%s:%s' % (GIT_LOGIN, AUTH_KEY)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	try:
		response = urllib2.urlopen(request)
		return response.read().strip()
	except urllib2.HTTPError, err:
		if err.code == 404:
			print str(user) + " : repos not found"
		else:
			print "Error " + str(err.code) + " : " + str(err.reason)
# ============ /FUNCTIONS =============


# ============= MAIN =============
# Get all Users
htmlText = requests.get(URL_GIT_USERS).text.encode('utf-8')
allUsers = re.findall('<td><a href="https://github.com/(.*?)">', htmlText, re.S) or None
if not allUsers:
	print 'No users found'
	sys.exit()
# We want to keep only NB_USERS users
allUsers = allUsers[:NB_USERS]

# For each user, compute the mean of each repository's stars
starsMean = {}
for user in allUsers:
	allReposJson = getJson(user)
	if allReposJson:
		allRepos = json.loads(allReposJson)
		sumStars = 0.0
		for repo in allRepos:
			sumStars += repo['stargazers_count']
		starsMean[user] = sumStars / len(allRepos)
		print str(user) + " : " + str(starsMean[user])

sortedStarsMean = sorted(starsMean.items(), key=operator.itemgetter(1), reverse=True)
print sortedStarsMean
# ============= /MAIN =============