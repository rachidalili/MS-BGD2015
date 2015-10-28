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
  
my_token = "yop"  
rqHeader = {"Authorization": "token "+my_token}
def connectWithToken(url):
    request = requests.get(url+"/user", headers=rqHeader)
    return request.status_code
    
def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup
    
def getRequestFromUrl(url):
    request = requests.get(url)
    print(request.text)
    return request, request.status_code


def main():
    connectWithToken(urlIdentification)
    request = getRequestFromUrl(urlToCrawl)
    print(request)
    #status = authentification()
    #print(status)
    #status = connectWithToken()
    #print(status)
        
if __name__ == '__main__':
    main()  
