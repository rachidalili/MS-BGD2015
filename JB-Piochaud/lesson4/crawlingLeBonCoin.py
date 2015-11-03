# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 21:02:59 2015

@author: jean-baptiste
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urlLeBonCoin = "http://www.leboncoin.fr/voitures/offres/"
urlLeBonCoin2 = "/?f=a&th=1&q=Renault+Zoé"
urlLaCentrale = "http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html"

region = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]

def getSoupFromUrl(url):
    request = requests.get(url)
    #print(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup
    
def getUrlListFromSoup(region):
    urlList = []
    soup = getSoupFromUrl(urlLeBonCoin + region + urlLeBonCoin2)
    urlSoup= soup.findAll('div', attrs= {'class' : 'list-lbc'})[0]
    for url in urlSoup.select('a'):
        urlList.append(url.attrs['href'])
    return urlList
    
def getInfoSellerFromUrl(url):
    priceList = []
    modelList = []
    yearList = []
    brandList = []
    descriptionList = []
    phoneNumberList = []
    
    for u in url:
        soup = getSoupFromUrl(u)
        #priceList.append(int(soup.findAll('span', attrs= {'class' : 'price'})[0].attrs['content']))
        #modelList.append(soup.findAll('td', attrs= {'itemprop' : 'model'})[0].text)
        #brandList.append(soup.findAll('td', attrs= {'itemprop' : 'brand'})[0].text)
        #regex = re.compile(r'[0-9]{4}')
        #year = regex.search(soup.findAll('td', itemprop='releaseDate')[0].text)
        #yearList.append(year.group())
        regex = re.compile(r'[0-9]{10}')
        phoneNumber = regex.search(soup.findAll('div', itemprop='description')[0].text)
        phoneNumberList.append(phoneNumber.group())
        #descriptionList.append(soup.findAll('div', itemprop='description')[0].text)
        
        
    return phoneNumberList
    
def main():
    #for r in region:
    urlList = getUrlListFromSoup(region[0])
    priceList = getInfoSellerFromUrl(urlList)
    print(priceList)
        #print(urlList)


if __name__ == '__main__':
    main()