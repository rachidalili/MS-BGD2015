import requests
from bs4 import BeautifulSoup
import pandas as pd

def FromTestToInt(txt):
   	return int(txt.replace(u'\xa0', u'').replace(u'\u20ac', u'').replace(' ',''))


def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def GetInformation(soup):
    like = GetButton(soup, "like-button-renderer-like-button")
    print 'like:', like
    dislike = GetButton(soup, "like-button-renderer-dislike-button")
    print 'dislike:', dislike
    nbview = soup.findAll("div", {"class": "watch-view-count"})[0].text
    intnbview = FromTestToInt(nbview)
    print 'NbView:', intnbview
    print('#####')

def recupKM(txt):
	return int(txt.replace(u'KM', u'').replace(u'\nKilom\xe9trage :', u'').replace(' ',''))

def typeversion(Alldes):
    if 'ZEN' or 'Zen' or 'zen' in Alldes.text:
    	return 'ZEN'
    if 'Life' or 'LIFE' or 'life'in Alldes.text:
    	return 'LIFE'
    if 'Intens' or 'INTENS' or 'intens'in Alldes.text:
    	return 'INTENS'


def coteLacentrale(modele,annee):
	url_cote='http://www.lacentrale.fr/cote-auto-renault-zoe-'+modele+'+charge+rapide-'+annee+'.html'
	soupCoteArgus = GetSoupFromUrl(url_cote)
	Cote = soupCoteArgus.find('span', {'class': 'Result_Cote arial tx20'})
	return FromTestToInt(Cote.text)




def GetSoupFromUrl(url):
	request=requests.get(url)
	return BeautifulSoup(request.text, 'html.parser')
	
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
	if annee in range(2012,2015):
		cote=(coteLacentrale(version,str(annee)))
		if cote>prix:
			CompareCoteToprice='low'
		else:
			CompareCoteToprice='high'
	else:
		cote='NA'
		CompareCoteToprice='NA'
	

	return str_name_region,version,annee,typevendeur,km,prix,cote,CompareCoteToprice


def LeBonCoinZoe(listregion):
	listcar=[]
	for str_name_region in listregion:
	
		url='http://www.leboncoin.fr/voitures/offres/'+str_name_region+'/?f=a&th=1&ps=14&q=renault+zoe'
		
		soup = GetSoupFromUrl(url)

		bloc_all_cars= soup.find('div', { 'class' : 'list-lbc' })
		cars = bloc_all_cars.findAll('a')
		for car in cars:
			
			if ('Renault') in car['title']:
				url_zoe=car['href']
				listcar.append(GetInformation(url_zoe,str_name_region))

	return listcar

listInfo=['Region','Version','Annee','Type de Vendeur','KM','Prix','Cote','Comparaisan Prix vs Cote']
listregion=['ile_de_france','aquitaine']
listALL=LeBonCoinZoe(listregion)

Result_DF = pd.DataFrame(listALL, columns=listInfo)



