# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 20:39:08 2015

@author: jean-baptiste
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

urlIdentification = "https://api.github.com"
urlToCrawl = "https://gist.github.com/paulmillr/2657075"

def authentification(url):
    url_dynamic = {'access_token': 'piochaud'}
    request = requests.get(url, headers = url_dynamic)
    return request.status_code
    
def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup
    
def getRequestFromUrl(url):
    request = requests.get(url)
    return request, request.status_code

def getTableFromSoup(soup):
    el = soup.findAll("table")
    #print(el[0].text)
    return el[0]
    
def getNamesFromTable(table):
    TableOfValues = ["unknown"]*256
    j = 1
    for i in range(0, 256):
            selectorRow = 'tr:nth-of-type(' + str(i+2) + ') '
            selectorCol = 'td:nth-of-type(' + str(j) + ')'
            selector = selectorRow + selectorCol
            #TableOfValues[i] = selector
            #print(table.select(selector)[2].text)
            TableOfValues[i] = table.select(selector)[0].text
            #TableOfValues[i] = TableOfValues[i].replace(u'\xa0', u'')
    return TableOfValues

def main():
    status = authentification(urlIdentification)
    print(status)
    #request = getRequestFromUrl(urlToCrawl)
    #print(request)
    soup = getSoupFromUrl(urlToCrawl)
    table = getTableFromSoup(soup)
    names = getNamesFromTable(table)
    print(names)


        
if __name__ == '__main__':
    main()  
