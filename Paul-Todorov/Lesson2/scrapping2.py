# coding: utf8
from pylab import *
import requests
from bs4 import BeautifulSoup

lignes = [10, 14, 22, 27]
postes = ['A','B','C','D']
colonnes = [2,3]
Years = [2010,2011,2012,2013] 

def extractIntFromText(text):
  return int(text.replace(u'\xa0', u'').replace(' ' ,''))

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getUrl(year):
    year = str(year)
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
    return url


   	
def getMetricsfromYear(year):
	listeeuro = []
	listestrate = []
	url =  getUrl(year)  
	soup = getSoupFromUrl(url)
	rapport = {}
	posteA = {}
	posteB = {}
	posteC = {}
	posteD = {}
	for ligne in lignes :
		
		Euro_parHab = soup.select('tr:nth-of-type('+ str(ligne) + ') > td:nth-of-type(' + str(colonnes[0]) + ')')
		Strate = soup.select('tr:nth-of-type('+ str(ligne) + ') > td:nth-of-type(' + str(colonnes[1]) + ')')
		Euro_parHab = extractIntFromText(Euro_parHab[0].text)
		Strate = extractIntFromText(Strate[0].text)
		listeeuro.append(Euro_parHab)
		listestrate.append(Strate)
	print "Euros par habitant"
	for k in range(len(listeeuro)) :
		print "poste " + str(postes[k]) + " = " + str(listeeuro[k])
	print "Moyenne de la strate"
	for k in range(len(listestrate)) :
		print "poste " + str(postes[k]) + " = " + str(listestrate[k])

	print 
	"======="

	rapport[year] = array([[listeeuro,listestrate]])
	
	
	return rapport






def getAllMetrics (k) :
	all_metrics = []
	for i in range (0,k):
		print Years[i]
		url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(Years[i])
		MetricsfromYear = getMetricsfromYear(Years[i])
		all_metrics.append(MetricsfromYear)
	return all_metrics

getAllMetrics(4)
