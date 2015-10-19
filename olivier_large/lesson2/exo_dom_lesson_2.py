import requests
from bs4 import BeautifulSoup

def testPage(soup):
	if str(soup.select(".montantpetit.G")) != "[]":
		return True
	else:
		return False

def getSoupFromUrl(url):
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getDataFromTab(soup,num_ligne,num_colonne):
	css_selector = "tr:nth-of-type(" + str(num_ligne) +") > td:nth-of-type(" + str(num_colonne) +")"
	data = soup.select(css_selector)[0].text.replace('\xa0', '').replace(' ','')
	return data

def getAllDataFromPage(annee) :
	#list format return is [A, B, C, D]
	title = ["A","B","C","D"]
	lignes = [10,14,22,27]
	colonnes = [2,3]
	all_data = []
	url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(annee)
	soup = getSoupFromUrl(url)
	test =testPage(soup)
	if(test is True):
		#select all class montantpetit G and td number under class bleu
		nb_data = 0
		for ligne in lignes:
			data = []
			data.append(title[nb_data])
			for colonne in colonnes:
				data.append(getDataFromTab(soup,ligne,colonne))
			all_data.append(data)
			nb_data += 1
	return all_data

def printDataForRange(annees):
	for i in range (annees[0],annees[1]+1):
		all_data = getAllDataFromPage(i)
		print("=== annee " + str(i) + " ===")
		print("euros par habitant - moyenne strate ")
		for el in all_data:
			print("--- " + el[0] + " :  " + el[1] + " - " + el[2] +"  ---")
		print(" ")
	return True

annees = [2009,2013]
printDataForRange(annees)


