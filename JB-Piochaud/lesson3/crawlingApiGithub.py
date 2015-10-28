# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 20:39:08 2015

@author: jean-baptiste
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

urlApi = "https://api.github.com"
urlToUser = "https://gist.github.com/paulmillr/2657075"

def authentification(url):
    url_dynamic = {'access_token': 'piochaud'}
    request = requests.get(url, headers = url_dynamic)
    print(request.text)
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
    TableOfNames = ["unknown"]*256
    j = 1
    for i in range(0, 256):
            selectorRow = 'tr:nth-of-type(' + str(i+2) + ') '
            selectorCol = 'td:nth-of-type(' + str(j) + ')'
            selector = selectorRow + selectorCol
            TableOfNames[i] = table.select(selector)[0].text
            TableOfNames[i] = str(TableOfNames[i].split(" ")[0])
            #TableOfValues[i] = TableOfValues[i].replace(u'\xa0', u'')
    return TableOfNames
    
def getStarsTableNames(url, tableNames):
    #for el in tableNames:
    urlUser = urlApi + "/users/" + tableNames[0] + "/repos"
    #print(urlUser)
    status = authentification(url)
    print(status)
    return urlUser

def main():
    status = authentification(urlApi)
    print(status)
    soup = getSoupFromUrl(urlToUser)
    table = getTableFromSoup(soup)
    tableNames = getNamesFromTable(table)
    #print(tableNames)
    getStarsTableNames(urlApi, tableNames)
   

if __name__ == '__main__':
    main()  
