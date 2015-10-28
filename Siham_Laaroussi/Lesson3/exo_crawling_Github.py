
# coding: utf-8

# In[63]:

__author__ = 'Sihamlaaroussi'

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import argparse


def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup
# 1ere question 
for row in soup.findAll('table')[0].tbody.findAll('tr'):
    rank = row.findAll('th')[0].text
    print 'Rank'+' '+ rank
    allinfos = row.findAll('td')[0].text
    print allinfos
    first_name = row.findAll('td')[0].text.split(' ')[1].replace('(','')
    last_name = row.findAll('td')[0].text.split(' ')[2].replace(')','')

    print " The user's name is: "+ first_name  + last_name
    second_column = row.findAll('td')[1].text
    print " Number of contributions : "+ second_column.replace('\u0',' ')
    print '----------------'
#2eme question





# In[ ]:



