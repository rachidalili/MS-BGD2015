import requests
from bs4 import BeautifulSoup


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

url_zoe = 'http://www.leboncoin.fr/voitures/846691426.htm?ca=12_s'
soupInfo = GetSoupFromUrl(url_zoe)
Pro = soupInfo.find('div', {'class': 'upload_by'})
pro2 = Pro.find('span', {'class': 'ad_pro'})

if pro2 is not None:
    ispro = 'yes'
else:
    ispro = 'no'
param = soupInfo.find('div', {'class': 'lbcParams criterias'})

km = recupKM(param.select('tr:nth-of-type(3)')[0].text)
annee=FromTestToInt(soupInfo.find('td', {'itemprop': 'releaseDate'}).text)
prix = FromTestToInt(soupInfo.find('span', {'class': 'price'}).text)

des = soupInfo.find('div', {'itemprop': 'description'})
version = typeversion(des)
cote=coteLacentrale('INTENS','2014')

