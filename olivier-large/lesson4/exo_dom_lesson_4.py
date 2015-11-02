import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
from getpass import getpass
from tabulate import tabulate

#Return soup from url
def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

#Return all datas in a sorted panda dataframe
def getAllCarUrl(zone_recherche):
	df = pd.DataFrame(columns=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel','argus','gooddeal'])
	for zone in zone_recherche:
		url = 'http://www.leboncoin.fr/voitures/offres/' + zone + '/?f=a&th=1&q=Renault+Zo%C3%A9'
		soupSearch = getSoupFromUrl(url)
		for a in soupSearch.select(".list-lbc > a"):
			soupCar = getSoupFromUrl(a['href'])
			brand = soupCar.find('td', {"itemprop":"brand"}).text
			model = soupCar.find('td', {"itemprop":"model"}).text
			if brand.lower() == 'renault' and model.lower() == 'zoe':
				v = re.search("(intens|life|zen)",soupCar.find('h1',{"itemprop":"name"}).text.lower())
				if v:
					version = v.group(1)
				annee = soupCar.find('td', {"itemprop":"releaseDate"}).text.strip()
				kilometrage_raw = soupCar.select(".lbcParams.criterias")[0].select("tr:nth-of-type(3) > td")[0].text.replace(" ","")
				kilometrage_reg = re.search("(.*)KM",kilometrage_raw)
				if kilometrage_reg:
					kilometrage = float(kilometrage_reg.group(1))
				prix_raw = soupCar.find('span', {"itemprop":"price"}).text
				prix_reg = re.search("(.*)€",prix_raw)
				if prix_reg:
					prix = float(prix_reg	.group(1).replace(" ",""))
				m = re.search("0[1-9][0-9]{8}",soupCar.find('div', {"itemprop":"description"}).text)
				if m:
				    telephone = m.group(0)
				professionnel = 'oui'
				pro = soupCar.find('span', {"class":"ad_pro"})
				if not pro:
					professionnel = 'non'
				urlArgus = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + version + '+charge+rapide-' + annee +'.html'
				soupArgus = getSoupFromUrl(urlArgus)
				argus_reg = re.search("(.*) €",soupArgus.select(".Result_Cote.arial.tx20")[0].text)
				if argus_reg:
					argus = float(argus_reg.group(1).replace(" ",""))
				if argus != 0:
					test = prix - argus
					if(test < -1000):
						gooddeal = "mega good deal"
					elif(-1000 <= test <= 0):
						gooddeal = "good deal"
					elif(0 <= test <= 1000):
						gooddeal = "bad deal"
					else:
						gooddeal = "very bad deal"
				else:
					gooddeal = "NA"

				df = df.append(pd.Series({'version':version, 'annee':annee, 'kilometrage':kilometrage, 'prix':prix, 'telephone':telephone, 'professionnel':professionnel,'argus':argus,'gooddeal':gooddeal}, index=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel', 'argus','gooddeal']), ignore_index=True)
	df.to_csv('zoe.csv')
	return(df)

def prettyPrint(listData):
	print(tabulate(listData, headers=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel', 'argus','gooddeal'], tablefmt='psql'))


zone_recherche = ["ile_de_france","provence_alpes_cote_d_azur","aquitaine"]
datas = getAllCarUrl(zone_recherche)
prettyPrint(datas)

