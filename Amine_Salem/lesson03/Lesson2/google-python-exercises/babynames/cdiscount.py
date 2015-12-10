# coding: utf8
import CrawlerArtist
import requests
import random
import sys
from threading import Thread
import time
import os
from bs4 import BeautifulSoup



def extractIntFromText(text):
  return int(text.replace(u'\xa0', u''))

def extractGenericLike(soup,classname):
  like_button = soup.findAll("button", { "class" : classname })[0]
  like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
  like_count = extractIntFromText(like_count_str)
  return like_count

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractFromUrl(url):

  soup = getSoupFromUrl(url)
  articles = soup.findAll('div', {'class':'prdtBloc'})
  for article in articles:
    name = article.find('div', {'class':'prdtBTit'})
    name = name.text.encode('utf-8')
    desc = article.find('p', {'class':'prdtBDesc'}).text.encode('utf-8')
    for oldprice in article.findAll('div', {'class':'prdtPrSt'}):
      oldprice = oldprice.text.encode('utf-8')
    price = article.find('span', {'class':'price'}).text.encode('utf-8')
# print desc
    print name
    print desc
    print oldprice
    print price
  # print soup.findAll('div', {'class':'prdtBTit'})

urlAcer = 'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
urlDell = 'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'

extractFromUrl(urlAcer)
extractFromUrl(urlDell)
