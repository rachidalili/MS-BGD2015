# coding: utf8

# Script crawling githbu contributors through API 
# Course INFMDI 721 - Lesson 3
# Author : Malik OUSSALAH



import requests
from bs4 import BeautifulSoup
from numpy import mean
import pandas as pd
import urllib2
import json


def authentification():
    """
    Since this script requires more than 60 API request / hours,
    we need to authentificate as a GitHub user.
    Returns:
    --------
    tuple (username, password)
    """
    username = str(input('GitHub username:'))
    password = str(input('GitHub password:'))
    r = requests.get('https://api.github.com/user', auth=(username, password))
    if r.status_code != 200:
        print('Incorrect username/password, please retry')
        return authentification()
    return (username, password)


def GetContributors(auth):
    """list of the most active users """
    users = {}
    r = requests.get(url='https://gist.github.com/paulmillr/2657075/',
            auth=auth)
    soup = BeautifulSoup(r.text,'html.parser')
    print " "
    print "Username " + "    " + " Contribution"
    print "#############################################"
    print " "
    for tr in soup('tbody')[0].select('tr'):
        user_name = tr.select('td')[0].text
        user_contrib = tr.select('td')[1].text
        users[user_name] = user_contrib
        #print user_name + " " + user_contrib
        print user_name, user_contrib

def GetJson(user):
    GIT_API_REPOS = "https://api.github.com/users/%user%/repos"
    req = urllib2.Request(url=GIT_API_REPOS.replace('%user%',user))
    response = urllib2.urlopen(req)
    return response.read().strip()


#TEST
r = requests.get(url='https://gist.github.com/paulmillr/2657075/',
            auth=("MalikOussalah","VX6yLCbv"))
soup = BeautifulSoup(r.text, 'html.parser')
#for tr in soup('tbody')[0].select('tr'):
#    print tr.select('td')[0].text
#prendre que le premier element
print soup('tbody')[0].select('td')[0].text.split(" ")[0]

#GetContributors(authentification())


          

