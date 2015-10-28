
# coding: utf-8

__author__ = 'Sihamlaaroussi'

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib2, base64
import json
import numpy as np


USER = 'sihamlaaroussi'
API_TOKEN ='afe208e08f43483b00adcc92d45dba789a31ba11'
GIT_API_URL='https://api.github.com/users/:username/repos'


def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def get_api(user):
    try:
        request = urllib2.Request(GIT_API_URL.replace(':username', user ))
        base64string = base64.encodestring('%s/token:%s' % (USER, API_TOKEN)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        return result.read()
        result.close()
    except:
        GIT_API_URL.replace(':username', user )
        print 'Failed to get api request from %s' % GIT_API_URL

# 1ere question
url = 'https://gist.github.com/paulmillr/2657075/'
soup = getSoupFromUrl(url)
array = np.empty([0, 5])
for row in soup.findAll('table')[0].tbody.findAll('tr'):
    rank = row.findAll('th')[0].text
    print 'Rank'+' '+ rank
    allinfos = row.findAll('td')[0].text
    print allinfos
    second_column = row.findAll('td')[1].text
    print "Number of contributions : "+ second_column.replace('\u0',' ')
    userrepo = row.select('td')[0].text.split(" ")[0]
    print userrepo
    strcontent = get_api(userrepo)
    jsoncontent = json.loads(strcontent)
    sum = 0
    counter = 0
    for content in jsoncontent:
        sum += content['stargazers_count']
        counter += 1
    mean = float(sum)/counter
    print 'Mean of all repositories stars: '+ str(mean)
    arow = [rank,allinfos,second_column.replace('\u0',' '),userrepo,mean]
    arow = np.expand_dims(arow, axis=0)
    array = np.append(array, arow, axis=0 )
    #print array[:,4]
    print '============================================='
sortedusers = sorted(array, key=lambda x: x[4], reverse=True)
print sortedusers

