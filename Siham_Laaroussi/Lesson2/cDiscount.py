__author__ = 'Sihamlaaroussi'

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def getAllInfos (soup):
    allblocs = soup.findAll("div", {"class": "prdtBloc"})
    for bloc in allblocs:
        print "----------------"
        Titre = bloc.find("div", {"class": "prdtBTit"}).text
        print Titre
        Infos = bloc.find("p", {"class": "prdtBDesc"}).text
        print Infos
        lien =bloc.find('a').get('href')
        print lien
        prices = bloc.find("div", {"class": "prdtBZPrice"})
        old_price = prices.find("div", {"class": "prdtPrSt"})
        if old_price is not None:
            print "Old price is: "+ str(old_price.text)
        new_price= bloc.find("span", {"class": "price"}).text
        print "New price is: " + new_price
        recommandations = bloc.find("div", {"class": "prdtBStar"}) 
        if recommandations is not None: 
            print str(recommandations.text)+" person recommanded this"
        #if old_price is not None and new_price is not None :
            #new_price.replace('€',',')
            #print type(new_price)
            #a = old_price.text.replace('u','')
            #print a
            #print new_price.replace('€','')
            #promotion = repr(old_price.text) - repr(new_price)/ repr(new_price) * 1000
            #print "Congrats ! You have a promotion of: "+ str(promotion) 
            #unsupported operand type(s) for -: 'unicode' and 'unicode'
            #invalid literal for float(): 349,00
soup = getSoupFromUrl("http://www.cdiscount.com/search/10/acer+aspire.html#_his_")
getAllInfos(soup)
