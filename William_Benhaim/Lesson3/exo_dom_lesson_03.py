# coding: utf8 #
import requests
from bs4 import BeautifulSoup
import json
import urllib2
import re
from requests.auth import HTTPBasicAuth
def GetSoupFromUrl(url):
	request=requests.get(url)
	return BeautifulSoup(request.text, 'html.parser')
def FromTestToInt(txt):
	return int(txt.replace(u'\u20ac',u' ').replace(' ',''))
def FromTextToTextWithPlus(txt):
	return txt.replace(' ','+')

#
# Connect to github api using token
#
def connectWithToken():
    request = requests.get(github_api_url+"/user", headers=rqHeader)
    return request.status_code

#

soup = GetSoupFromUrl('https://gist.github.com/paulmillr/2657075')
allbigContribs = soup.findAll("tr", { "td" : "" })
#allbigContribs = soup.select('tr > td:nth-of-type(1)')
Liste_names=[]

for bc in allbigContribs:
	#bigContrib = bc.findAll("a")
	#print bc
	bigContrib = bc.select('td:nth-of-type(1) > a')
	for el in bigContrib:
		Liste_names.append({'user':el.text})

for nbLS in range(len(Liste_names)):
	urlApi= 'https://api.github.com/users/'+Liste_names[nbLS]['user']+'/repos'
	resp = requests.get(url=urlApi,auth=('williamben','***')) # rajouter le mot de passe. a ameliorer
	data = json.loads(resp.text)
	sommestargazers=0.0
	for SG in data:
		sommestargazers += float(SG['stargazers_count'])
	Liste_names[nbLS]['res_stargazers']=sommestargazers/len(data)
	print 'user:'+Liste_names[nbLS]['user'], 'stargazers:'+str(Liste_names[nbLS]['res_stargazers'])



print type(Liste_names)
sorted_users = sorted(Liste_names,key=lambda types: types['res_stargazers'])
for sortuser in sorted_users:
	print ('user:'+sortuser['user'],sortuser['res_stargazers'])
# 	res = requests.get('https://api.github.com/users/'+el.text+'/repos').json()
	# 	print res
