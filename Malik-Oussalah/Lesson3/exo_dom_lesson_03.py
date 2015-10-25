# coding: utf8

# Script tested with Python 3.5.0 and 2.7.10
# Course INFMDI 721 - Lesson 3
# Author : Guillaume MOHR

# IMPORTANT   : the script nees an authentification to GitHub
#               In order to execute it, a valide username / password
#               or username / token have to be submitted at the prompt

# To improve compatibility with Python 2.x:
from __future__ import unicode_literals 

import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from numpy import mean
import pandas as pd


def authentification():
    """
    Since this script requires more than 60 API request / hours,
    we need to authentificate as a GitHub user.
    Returns:
    --------
    tuple (username, password)
    """
    username = input('GitHub username:')
    password = input('GitHbu password:')
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
    for tr in soup('tbody')[0].select('tr'):
        user_name = tr.select('td')[0].text
        user_contrib = tr.select('td')[1].text
        users[user_name] = user_contrib
        #print user_name + " " + user_contrib
    print users.items()


r = requests.get(url="https://api.github.com/users/Ocramius/repos",auth=("MalikOussalah","VX6yLCbv"))
soup = BeautifulSoup(r.text, 'html.parser')
#TEST
#r = requests.get(url='https://gist.github.com/paulmillr/2657075/',
 #           auth=("MalikOussalah","VX6yLCbv"))
#soup = BeautifulSoup(r.text, 'html.parser')
#for tr in soup('tbody')[0].select('tr'):
#    print tr.select('td')[0].text
#print soup('tbody')[0].select('td')[0].text

#GetContributors(authentification())
        
            

