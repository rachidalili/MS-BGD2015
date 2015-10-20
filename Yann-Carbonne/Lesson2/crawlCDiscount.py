#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
	print "No search criteria"
	sys.exit()

# CONFIGURATION
url = "http://www.cdiscount.com/search/10/%SEARCH%.html"
criteria = sys.argv[1:]

def getUrl(criterion):
    return url.replace('%SEARCH%', criterion.lower().replace(" ", "+"))

def getSoup(criterion):
	url = getUrl(criterion)
	request = requests.get(url)
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def getEntries (soup):
	return soup.findAll('div', {'class': 'prdtBloc'})

for criterion in criteria:
	print "=========================== " + str(criterion) + " ==========================="
	for entry in getEntries(getSoup(criterion)):
		print "=============="
		print "Url : " + str(entry.find('a').get('href'))
		print "Title : " + str(entry.find('div', {'class': 'prdtBTit'}).get_text().encode('utf-8'))
		print "Image : " + str(entry.find('ul', {'class': 'prdtBPCar'}).find('img')['src'])
		print "Price : " + str(entry.find('span', {'class': 'price'}).get_text().encode('utf-8'))
		oldPrice = entry.find('div', {'class': 'prdtPrSt'})
		print "Old price : " + str(oldPrice.get_text().encode('utf-8') if oldPrice else "")
		print "=============="	