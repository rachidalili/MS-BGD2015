# coding: utf8

import requests
from bs4 import BeautifulSoup
import re


def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup


def getProductInfo(soup):
     entries= soup.findAll('div', {'class':'prdtBloc'})
     for entry in entries:


def getCdDiscountRef():
    for product in ['Acer aspire']:
        product=product.replace(" ","+")
        url = 'http://www.cdiscount.com/search/10/'+product+'.html#_his_'
        soup = getSoupFromUrl(url)
        getProductInfo(soup)




getCdDiscountRef()

