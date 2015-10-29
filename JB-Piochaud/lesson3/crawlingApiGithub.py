# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 20:39:08 2015

@author: jean-baptiste
"""
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import json

urlApi = "https://api.github.com"
urlToUser = "https://gist.github.com/paulmillr/2657075"
myHeaders = {'access_token': 'piochaud'}

def authentification(urlStatic, headers):
    request = requests.get(urlStatic, headers = myHeaders)
    if (request.status_code != 200):
        print("Connection problem to " + urlStatic)
        sys.exit(0)
    else:
        print("Connection OK to " + urlStatic)
    #print(request.text)
    return request.status_code
    
def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup
    
def getRequestFromApi(urlApi, myHeaders):
    request = requests.get(urlApi, headers = myHeaders)
    return request

def getTableFromSoup(soup):
    el = soup.findAll("table")
    #print(el[0].text)
    return el[0]
    
def getUsersFromTable(table):
    tableOfUsers = ["unknown"]*256
    j = 1
    for i in range(0, 256):
            selectorRow = 'tr:nth-of-type(' + str(i+2) + ') '
            selectorCol = 'td:nth-of-type(' + str(j) + ')'
            selector = selectorRow + selectorCol
            tableOfUsers[i] = table.select(selector)[0].text
            tableOfUsers[i] = str(tableOfUsers[i].split(" ")[0])
            #TableOfValues[i] = TableOfValues[i].replace(u'\xa0', u'')
    return tableOfUsers


def getJasonRequestFromApi(urlApiUser, myHeaders):
    r = requests.get(urlApiUser, headers = myHeaders)
    if (r.status_code != 200):
        print("Connection problem to " + urlApiUser)
        sys.exit(0)
    else:
        print("Connection OK to " + urlApiUser)
    #print(request.text)
    return r

#!def getStarsTableNames(urlStatic, myHeaders, tableNames):

def getMeanStarsRepoUserFromJason(tableOfUsers):
    meanStarsUserTable = []    
    #for i in range(1, len(tableOfUsers)):
    for i in range(1, 5):
        #page = {'page': }
        urlApiUser = urlApi + "/users/" + tableOfUsers[i-1] + "/repos"
        r = getJasonRequestFromApi(urlApiUser, myHeaders)
        reposUser = json.loads(r.text)
        meanStarsUser = 0
        for repo in reposUser:
            meanStarsUser = meanStarsUser + int(repo["stargazers_count"])
        meanStarsUser = meanStarsUser / float(len(reposUser))
        meanStarsUserTable.append(meanStarsUser) 
    return meanStarsUserTable

def main():
    authentification(urlApi, myHeaders)
    soup = getSoupFromUrl(urlToUser)
    table = getTableFromSoup(soup)
    tableOfUsers = getUsersFromTable(table)
    meanStarsUsers = getMeanStarsRepoUserFromJason(tableOfUsers)
    print(meanStarsUsers)
   

if __name__ == '__main__':
    main()  
