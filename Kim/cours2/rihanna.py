# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:57:36 2015

@author: kim
"""
import sys, os
from lxml import html
import requests
from bs4 import BeautifulSoup
import urllib2 #methode non conseillée
print requests.__version__
import json
import re


def getmetrics( soup ):
    
    for node in soup.findAll('div', {'class' : "watch-view-count"}):
        print "view count is", node.text

    likebutton= soup.findAll("button", {'class' : "like-button-renderer-like-button"})[0]
    for node in likebutton.findAll('span', {'class' : "yt-uix-button-content"}):
        print "like count is", node.text
    
    dislikebutton= soup.findAll("button", {'class' : "like-button-renderer-dislike-button"})[0]   
    for node in dislikebutton.findAll('span', {'class' : "yt-uix-button-content"}):
        print "dislike count is", node.text

#with request package
url = u'https://www.youtube.com/watch?v=2LT23ixDaJo'
print url
r = requests.get(url,  stream=True)
#print r.headers['content-type']


soup = BeautifulSoup(r.text) ## when using requests.get
getmetrics(soup)


