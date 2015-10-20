# coding: utf8

import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
	#Execute q request toward Youtube
	request = requests.get(url)
	#parse the restult of the request
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def extractPostFromPage(url):
	soup = getSoupFromUrl(url)
	# body = soup.find_all('div', {'class': 'content'})
	blocs = soup.find_all('div', {'class': 'prdtBloc'})
	for bloc in blocs:
		html = bloc.find('a').get('href')
		descr = bloc.find('p', {'class': 'prdtBDesc'}).text.encode('utf-8')
		price = bloc.find('span',{'class':'price'}).text.encode('utf-8')
		print html
		print descr
		print price

	return

def extractMetrics(bloc):
	url = bloc.find
	return


def main():
	extractPostFromPage('http://www.cdiscount.com/search/10/dell+xps+15.html#_his_')



if __name__ == '__main__':
	main()