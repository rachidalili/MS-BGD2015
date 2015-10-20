# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:40:37 2015

@author: varieux
"""

# coding: utf8

import requests
from bs4 import BeautifulSoup


def extractIntFromText(text):
  return int(text.replace(u'\xa0', u''))

 url = 'https://www.cdiscount.fr' + tile_link[]
 
 
def getSoupFromUrl(url):          
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractMetricsFromUrl(url):

  soup = getSoupFromUrl(url)
  #GEt Image
  view_Image = soup.findAll("img", { "class" : "jsExtZoom" })
  view_Image = extractIntFromText(view_image_)
  
  #GEt Description
  view_description = soup.findAll("p", { "class" : "itemprop" })[0].text
  view_description = extractIntFromText(view_description_)

#GEt prix
  view_prix = soup.findAll("p", { "class" : "fpRice price" })[0].text
  view_prix = extractIntFromText(view_prix_)

  