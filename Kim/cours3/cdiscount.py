# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:40:05 2015

@author: kim
"""
import requests
from bs4 import BeautifulSoup


def fromUrltoSoup( url):
    r = requests.get(url,  stream=True)
    return BeautifulSoup(r.text, 'html.parser')


def getmetrics( soup ):    
    print "****************Acer Aspire*********************"    
    bloc= soup.findAll("div", {'class' : "prdtBloc"})
    for i in range(0, len(bloc)):
        bloc_i = bloc[i]
        title= bloc_i.find("div", {'class' : "prdtBTit"})
        print "Titre: ",title.text
        price= bloc_i.find("span", {'class' : "price"})
        print "Prix: ",price.text
        lien_img= bloc_i.find("img", {'class' : "prdtBImg"})['src']
        print "Lien_img: ",lien_img

url = u'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
fromUrltoSoup( url) 
getmetrics(fromUrltoSoup( url))