# coding: utf8
import requests
import random
import sys
from threading import Thread
import time
import os
import re
from bs4 import BeautifulSoup
import pandas as pd

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def checkVoiture(soup):
	return soup.find(itemprop='brand').text == 'Renault' and soup.find(itemprop='model').text == 'Zoe'

def getUrl():
	return ['http://www.leboncoin.fr/voitures/offres/{}/?f=a&th=1&q=Renault+zoe'.format(region) for region in regions] 

def getAllUrlSearch(soup):
	links = soup.findAll('a')
	return [link['href'] for link in links]

def getPrice(soup):
	return float(soup.find('span', {'class':'price'})['content'])

def proOrParti(soup):
	return len(soup(class_='ad_pro')) > 0

def getVersion(soup):
	rexp = re.compile(r'(intens|life|zen)', re.IGNORECASE)
	title = soup.find('h1', {'id':'ad_subject'}).text
	return rexp.search(title).group().lower() if rexp.search(title) is not None else ''

def getModel(soup):
	return soup.find(itemprop='model').text

def getAnnee(soup):
	return re.sub(r'[ \n]', '', soup.find(itemprop='releaseDate').text)

def getKM(soup):
	return re.sub(r'[ KM]','', soup.find('div', {'class':'lbcParams criterias'}).select("tr:nth-of-type(3) > td")[0].text)

def getTelephone(soup):
	textContent = unicode(soup.find('div', {'class': 'content'}))		
	rexp = re.compile('((?:[0-9]{2}[ .-]*){5})')
	return re.sub(r'[ .-]', '', rexp.search(textContent).groups()[0]) if rexp.search(textContent) is not None else ''

def getInformation(links):
	for link in links:
		soup = getSoupFromUrl(link)
		lien.append(link)
		list_version.append(getVersion(soup))
		list_pro.append('pro' if proOrParti(soup) else 'parti')
		list_annee.append(getAnnee(soup))
		list_prix.append(int(getPrice(soup)))
		list_KM.append(getKM(soup))
		list_model.append(getModel(soup))
		list_telephone.append(getTelephone(soup))

def getPriceArgus(model, year):
	url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + model + '+charge+rapide-' + year + '.html'
	soup = getSoupFromUrl(url)
	prix = soup.find('span', {'class':'Result_Cote arial tx20'}).text
	price_model_year[model, year] = int(re.sub(r'[^0-9]', '', prix))
	return price_model_year[model, year]
	
def informationToDF():
	df = pd.DataFrame(data = {
        'Lien': lien,
        'Annee':list_annee,
        'Version':list_version,
        'Pro ou Parti': list_pro,
        'Telephone': list_telephone,
        'KM':list_KM,
        'Prix': list_prix,
        'Model': list_model
    	})
	df['PrixArgus'] = df.apply(lambda row: price_model_year.get((row.Version, row.Annee)), axis=1)
	return df








list_prix = []
list_version = []
lien = []
list_pro = []
price_model_year = {}
list_model = []
list_annee = []
list_KM = []
list_telephone = []
regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
versions = ['intens', 'life', 'zen']
years = ['2012','2013','2014']
list_url_region = getUrl()

for url in list_url_region:
	soup = getSoupFromUrl(url)

	# On est sur le bloc qui contient toutes les annonces
	listblc = soup.find('div', {'class':'list-lbc'})
	voitures_annonces = listblc.findAll('div', {'class':'lbc'})

	# On recupere les informations annonce par annonce
	list_url_annonce = getAllUrlSearch(listblc)
	mask = [checkVoiture(getSoupFromUrl(link)) for link in list_url_annonce]
	lien_correct = [l for m, l in zip(mask, list_url_annonce) if m]
	getInformation(lien_correct)

price_argus = [getPriceArgus(m,y) for y in years for m in versions]
DF = informationToDF()
print DF


