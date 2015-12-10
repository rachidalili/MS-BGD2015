import pandas as pd
import requests
import re
import json


URL = 'https://gist.github.com/paulmillr/2657075'
# TOKEN_GIT TO DO

def request():
    r = requests.get(URL)
    text = r.text.encode('utf-8')
    return text

def regextext(text):
    p = re.compile('<td><a href="https://github.com/(.*?)">')
    m = p.findall(text)
    return m

def requestAPI(user):
	url = 'https://api.github.com/users/' + user + '/repos'
	headers = {'Authorization': 'token %s' % TOKEN_GIT}
	r = requests.get(url, headers=headers)
	return r.text.encode('utf-8')

def getMean(jsonRepos):
	total = 0.0
    	for repo in jsonRepos:
    		total += repo['stargazers_count']
    	mean = total / len(jsonRepos)
	return mean

def main():
    text = request()
    users = regextext(text)
    meanDict = {}
    for user in users:
    	repos = requestAPI(user)
    	jsonRepos = json.loads(repos)
    	mean = getMean(jsonRepos)
    	meanDict[user] = mean

    for k,v in meanDict.iteritems():
    	print k +': ' + str(v)

if __name__ == '__main__':
    main()