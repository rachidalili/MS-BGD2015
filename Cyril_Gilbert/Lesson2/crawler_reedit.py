# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:37:57 2015

@author: Cyril Gilbert
"""
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
url='http://www.cdiscount.com/informatique/ordinateurs-pc-portables/acer-ordinateur-portable-aspire-e5-721-437k-amd-a4/f-1070992-nxmndef031.html#mpos=1|cd'
soup=getSoupFromUrl(url)

description= soup.findAll("p", { "itemprop" : "description"})[0]
#price_striked= soup.findAll("p", { "class" : "fpSriked"})[0]
price_current= soup.findAll("p", { "itemprop" : "price"})[0]
#produit=soup.findAll("ul", { "id" : "lpBloc"})
#print(table[0].text)

#liste des produits
url='http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
soup=getSoupFromUrl(url)
liste=soup.findAll("div", { "class" : "prdtBloc"})