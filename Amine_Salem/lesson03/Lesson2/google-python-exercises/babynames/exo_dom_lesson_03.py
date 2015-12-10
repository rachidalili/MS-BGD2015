# coding: utf8

# Script crawling githbu contributors through API 
# Course INFMDI 721 - Lesson 3
# Author : Malik OUSSALAH

#Package Importation############

import requests
from bs4 import BeautifulSoup
import urllib2, base64
import operator
import json

################################



#Configuration####################################################

GIT_LOGIN = 'MalikOussalah'
# Get your token there : https://github.com/settings/tokens/new
AUTH_KEY = '9442e5ba8bd8ef216367008f9c9341500d59fc99'

##################################################################

#Function needed###############################################################

def start(auth):
    """function to get all repo users sorted by mean of stars"""
    users = {}
    r = requests.get(url='https://gist.github.com/paulmillr/2657075/',
            auth=auth)
    soup = BeautifulSoup(r.text,'html.parser')
    print " "
    print "Username " + "    " + " Contribution" + "       " + " Mean_Stars"
    print "###################################################################"
    print " "
    starsMean = {}
    for tr in soup('tbody')[0].select('tr'):
        user_name = tr.select('td')[0].text
        user_contrib = tr.select('td')[1].text
        users[user_name] = user_contrib
        user_repo = tr.select('td')[0].text.split(" ")[0]
        user_json = GetJson(user_repo)
        if user_json:
            allrepos = json.loads(user_json)
            sumstars = 0.0
            for el in allrepos:
                sumstars += el['stargazers_count']
            starsMean[user_repo] = sumstars / len(allrepos)
        #print user_name + " " + user_contrib
        print user_name, user_contrib, starsMean[user_repo]
        sortedMean = sorted(starsMean.items(), key=operator.itemgetter(1), reverse=True)
    print sortedMean

def GetJson (user):
    """function that get you the Json format of a user repo"""
    URL_GIT_API_REPOS_BY_USER = 'https://api.github.com/users/%USER%/repos'
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

###############################################################################

#Main###############################

start(("MalikOussalah","VX6yLCbv"))

####################################
          

