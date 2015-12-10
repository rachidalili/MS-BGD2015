# coding: utf8

import requests
from bs4 import BeautifulSoup


syntaxList = {1: "Euros par habitant pour A", 2: "Moyenne de la strate pour A", 
				 4: "Euros par habitant pour B", 5: "Moyenne de la strate pour B",
				 7: "Euros par habitant pour C", 8: "Moyenne de la strate pour C",
				 10: "Euros par habitant pour D", 11: "Moyenne de la strate pour D"}

# Get content from url
def getContentFromUrl(url):
	# Execute a request to get the content from a web page
	request = requests.get(url)
	# Parse the document
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def extractRow(ro, letterList, final):
	if len(ro) > 3:
			split = ro[3].text.encode('utf-8').split('=')
			if len(split) == 2:
				for letter in letterList:
					if split[1].strip() == letter:
						final.append(ro[3].text.replace(u'\xa0', u''))
						final.append(ro[1].text.replace(u'\xa0', u''))
						final.append(ro[2].text.replace(u'\xa0', u''))
	return

def extractNumber(soup):
	table = soup.find_all('table')
	#  if table is not empty
	final = []
	if table:
		table = soup.find_all('table')[2]
		rows = table.find_all('tr', {'class' : 'bleu'})
		letterList = ['A','B','C','D','E']
		for row in rows:
			ro = row.find_all('td')
			extractRow(ro, letterList, final)
	return final

def main():
	URL = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
	YEARS = range(2009, 2014)
	for year in YEARS:
		print '\n########\n  ' + str(year) + '\n########\n'
		soup = getContentFromUrl(URL + str(year))
		result = extractNumber(soup)

		if len(result) > 0:
			for num in syntaxList:
				print syntaxList[num] + "\t:\t" + str(result[num])
		else:
			print "No Data Found"



if __name__ == '__main__':
	main()