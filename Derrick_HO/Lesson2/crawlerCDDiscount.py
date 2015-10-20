# coding: utf8

import requests
from bs4 import BeautifulSoup


URL = 'http://www.cdiscount.com/search/10/'
END_URL = '.html#_his_'

Acer = URL + 'acer+aspire' + END_URL


def getSoupFromUrl(url):
	#Execute q request toward Youtube
	request = requests.get(url)
	#parse the restult of the request
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def extractPostFromPage(url):
	soup = getSoupFromUrl(url)
	# body = soup.find_all('div', {'class': 'content'})
	body = soup.find(id='lpContent')
	blocs = body.find_all(id='lpBloc')
	for bloc in blocs:
		print bloc.prettify().encode('utf-8')
		break
	return

def extractMetrics(bloc):
	url = bloc.find
	return


def main():
	extractPostFromPage('http://www.cdiscount.com/search/10/dell+xps+15.html#_his_')



if __name__ == '__main__':
	main()