# encoding: utf-8
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import phonenumbers
import numpy as np

# CONFIGURATION
REGIONS = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
VERSIONS = ['intens', 'zen', 'life']
URL_SEARCH_LBC = 'http://www.leboncoin.fr/voitures/offres/{region}/?o={num_page}&q=Renault+Zoe'
URL_ARGUS = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide-{year}.html'
OUTPUT_CSV = 'leboncoin_renault_zoe.csv'

# ======================================= FUNCTIONS =======================================

def getCarLinksForRegion (regionName):
	""" Give me a region name for LBC and I give you an array with all links for Zoe ads """
	allLinks = []
	allLinksFromPage = [' ']
	numPage = 1
	# Get through all pages of a search 
	while len(allLinksFromPage):
		url = URL_SEARCH_LBC.format(region=region, num_page=str(numPage))
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')
		allLinksFromPage = soup.findAll('a', href=re.compile('http://www.leboncoin.fr/voitures/\d{9}.htm'))
		allLinks += [e['href'] for e in allLinksFromPage]
		numPage += 1
	return allLinks

# ======================================= /FUNCTIONS =======================================


# ======================================= MAIN =======================================

# GET DATAS FROM LBC
df = pd.DataFrame(columns=['Version', 'Year', 'Mileage', 'Price', 'Phone Number', 'isPro'])
cpt = 0
for region in REGIONS:	
	adsLinks = getCarLinksForRegion(region)
	for adUrl in adsLinks:
		soup = BeautifulSoup(requests.get(adUrl).text, 'html.parser')

		# First, check car's model
		model = soup.find('td', itemprop='model').renderContents().strip().lower() or None
		if not model == "zoe":
			continue

		# Pro ?
		isPro = soup.find('span', {"class": "ad_pro"}) != None
		
		# Year
		year = int(soup.find('td', itemprop='releaseDate').renderContents().strip()) or None
		
		# Mileage
		mileage = int(re.sub('\D', '', soup.find(text='Kilométrage :').next.next.next)) or None

		# Price
		price = int(soup.find('span', {'class': 'price'})['content']) or None
		
		# Version
		title = soup.find('h1', id='ad_subject').get_text().lower() or None
		version = ''.join(set(VERSIONS).intersection(title.split(' '))) # Get version name if in title
		
		# Phone : Too lazy to click, just search for phone numbers in the ad
		textContent = unicode(soup.find('div', {'class': 'content'}))		
		phones = ""
		for match in phonenumbers.PhoneNumberMatcher(textContent, "FR"):
			phones += str(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)) + " "
		phones = phones[:-1] if phones else None

		# Add everything
		df.loc[cpt] = [version, year, mileage, price, phones, isPro]
		cpt += 1


# GET RATINGS FOR EACH VERSION/YEAR
df['RatingPrice'] = None
for year in np.unique(df[['Year']].values):
	for version in VERSIONS:
		url = URL_ARGUS.format(version=version, year=year)
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')
		rating = int(re.sub('\D', '', soup.find('span', {'class':  'Result_Cote'}).text))
		df.ix[(df.Year == year) & (df.Version == version), 'RatingPrice'] = rating # MaJ of rows with the specific year/version
df['BetterThanRating'] = df.apply(lambda row: (row.Price < row.RatingPrice if not (row.Price is None or row.RatingPrice is None) else None ), axis=1)

df.to_csv(OUTPUT_CSV, index=False)

# ======================================= /MAIN =======================================
