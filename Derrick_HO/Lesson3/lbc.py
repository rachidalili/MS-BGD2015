# coding: utf8

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL ='http://www.leboncoin.fr/voitures/offres/%LOCATION/?f=a&th=1&q=Renault+Zoe&it=1'

U = 'http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&q=Renault+Zoe&it=1'

LOCATION = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']

VERSION = ['life', 'zen', 'intens']

def getSoupFromUrl(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def getData(text):
	p = re.compile('<a href=(.*?)</a>')
	m = p.findall(text)
	return m

def getVersion(title):
	version = ''
	for s in VERSION:
		m = re.search(s, title.lower())
		if m:
			version = m.group(0)
			break

	return version


def initDict():
	itemDict = {}
	itemDict['version'] = ''
	itemDict['annee'] = ''
	itemDict['kilometrage'] = ''
	itemDict['prix'] = ''
	itemDict['tel'] = ''
	itemDict['categorie'] = ''

	return itemDict

def getAttribute(dic, attribute, value):
	line = (re.sub(':', '', attribute)).lower()

	d1 = re.search('année-modèle', line)
	if d1:
		dic['annee'] = value
	d2 = re.search('kilométrage', line)
	if d2:
		result = re.sub('[^0-9]','', value)
		dic['kilometrage'] = result

	return dic

def buildDict(dic, version, price, category, number, year, kilometrage):
	if version:
		dic['version'] = version
	if price:
		dic['prix'] = price
	if category:
		cat = re.search(r'\((.*?)\)',category).group(1)
		dic['categorie'] = cat
	if number:
		dic['tel'] = number
	if year:
		dic['annee'] = year
	if number:
		dic['kilometrage'] = kilometrage
	# if location:
	# 	dic['location'] = location
	return dic

def getNumber(text):
	d1 = re.search(r'\d{10}', text)
	number = None
	if d1:
		number = d1.group(0)
	return number

def getYear(text):
	rYear = re.search(r'\d{4}', text)
	year = None
	if rYear:
		year = rYear.group(0)
	return year

def getKm(text):
	rKm = re.search(r'Kilométrage :\n(.*?)\n', text)
	km = None
	if rKm:
		km = re.sub('[^0-9]','', rKm.group(1))
	return km

def extractPostFromPage(soup):
	body = soup.find_all('div', {'class': 'content-border list'})
	bloc = body[0].find_all('div', {'class': 'list-lbc'})
	ahref = bloc[0].find_all('a')
	mainDoc = {}
	i=0
	for a in ahref:
		itemDict = initDict()

		title = a.get('title')
		version = getVersion(title)
		link = a.get('href')
		category = a.find('div', {'class': 'category'}).text
		rawPrice = a.find('div', {'class': 'price'}).text.encode('utf-8')

		numeric = re.compile(r'[^\d]+')
		price = numeric.sub('', rawPrice)

		web = getSoupFromUrl(link)
		description = web.find('div', {'class': 'lbcParams criterias'})

		content = web.find('div', {'class': 'content'})

		number = getNumber(content.text)
		rows = description.find_all('tr')

		year = getYear(description.text.encode('utf-8'))

		km = getKm(description.text.encode('utf-8'))

		# for row in rows:
		# 	attribute = row.find('th').text.encode('utf-8')
		# 	value = row.find('td').text.encode('utf-8')
		# 	itemDict = getAttribute(itemDict, attribute, value)

		itemDict = buildDict(itemDict, version, price.strip(), category.strip(), number, year, km)

		mainDoc[i] = itemDict
		i+=1
	return mainDoc

def main():
	mainDict = {}
	for location in LOCATION:
		text = getSoupFromUrl(URL.replace('%LOCATION', location))
		itemDict = extractPostFromPage(text)
		mainDict[location] = itemDict


	# for k,v in mainDict.iteritems():
	# 	print k
	# 	print v

	print pd.DataFrame(mainDict)



if __name__ == '__main__':
	main()