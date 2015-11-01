import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def FromTestToInt(txt):
   	return int(txt.replace(u'\xa0', u'').replace(u'\u20ac', u'').replace(' ',''))


def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')

def recupKM(txt):
	return int(txt.replace(u'KM', u'').replace(u'\nKilom\xe9trage :', u'').replace(' ',''))

def typeversion(Alldes):
    if 'ZEN' in Alldes.text or 'Zen' in Alldes.text or 'zen' in Alldes.text:
    	return 'ZEN'
    if  'Life' in Alldes.text or 'LIFE' in Alldes.text or 'life' in Alldes.text:
    	return 'LIFE'
    if 'INTENS' in Alldes.text or 'Intens' in Alldes.text or 'intens' in Alldes.text:
    	return 'INTENS'


def coteLacentrale(modele,annee):
	url_cote='http://www.lacentrale.fr/cote-auto-renault-zoe-'+modele+'+charge+rapide-'+annee+'.html'
	soupCoteArgus = GetSoupFromUrl(url_cote)
	Cote = soupCoteArgus.find('span', {'class': 'Result_Cote arial tx20'})
	return FromTestToInt(Cote.text)


def GetInformation(url_zoe,str_name_region):
	listinfo=[]
	soupInfo = GetSoupFromUrl(url_zoe)
	des = soupInfo.find('div', {'itemprop': 'description'})
	version = typeversion(des)
	listinfo.append(version)
	annee=FromTestToInt(soupInfo.find('td', {'itemprop': 'releaseDate'}).text)
	listinfo.append(annee)

	Pro = soupInfo.find('div', {'class': 'upload_by'})
	pro2 = Pro.find('span', {'class': 'ad_pro'})

	if pro2 is not None:
	    typevendeur = 'Pro'
	else:
	    typevendeur = 'Perso'

	listinfo.append(typevendeur)
	param = soupInfo.find('div', {'class': 'lbcParams criterias'})

	km = recupKM(param.select('tr:nth-of-type(3)')[0].text)
	listinfo.append(km)
	prix = FromTestToInt(soupInfo.find('span', {'class': 'price'}).text)
	listinfo.append(prix)
	if annee in range(2012,2015) and version is not None:
		cote=(coteLacentrale(version,str(annee)))
		if cote>prix:
			CompareCoteToprice='low'
		else:
			CompareCoteToprice='high'
	else:
		cote='NA'
		CompareCoteToprice='NA'
	expression = r"0[0-9]([ .-/]?[0-9]{2}){4}"
	#phone=re.search(expression,des)

	isphone= re.search(expression,str(des))
	if isphone:
		phone=isphone.group()
	else:
		phone='NA'
	return str_name_region,version,annee,typevendeur,phone,km,prix,cote,CompareCoteToprice

def isZoe(libelle):
	return "Zo" in libelle or "zo" in libelle or "ZO" in libelle


def LeBonCoinZoe(listregion):
	listcar=[]
	for str_name_region in listregion:
	
		url='http://www.leboncoin.fr/voitures/offres/'+str_name_region+'/?f=a&th=1&ps=14&q=renault+zoe'
		
		soup = GetSoupFromUrl(url)

		bloc_all_cars= soup.find('div', { 'class' : 'list-lbc' })
		cars = bloc_all_cars.findAll('a')
		for car in cars:
			
			if isZoe(car['title']):
				url_zoe=car['href']
				listcar.append(GetInformation(url_zoe,str_name_region))

	return listcar

listInfo=['Region','Version','Annee','Type de Vendeur','Telephone','KM','Prix','Cote','Comparaisan Prix vs Cote']
listregion=['ile_de_france','aquitaine','provence_alpes_cote_d_azur']
listALL=LeBonCoinZoe(listregion)

Result_DF = pd.DataFrame(listALL, columns=listInfo)
print Result_DF


