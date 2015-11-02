# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:29:05 2015

@author: cgilbert
"""
import requests
from bs4 import BeautifulSoup

def getContentFromUrl(url):
	# Execute a request to get the content from a web page
	request = requests.get(url)
	# Parse the document
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

url='http://www.leboncoin.fr/annonces/offres/ile_de_france/?f=a&th=1&q=Renault+Zo%C3%A9'

soup = getContentFromUrl(url);

list_bloc=soup.find("div", { "class" : "list-lbc" })
list_article=list_bloc.findAll('a',href=True)

for i in range(len(list_article)):
    text=str(list_article[i].find("div", { "class" : "category" }))#.replace(" ","")
    print(str(text))