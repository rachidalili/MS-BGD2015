import requests
from bs4 import BeautifulSoup


page = requests.get('http://www.cdiscount.com/search/10/acer+aspire.html#_his_')

soup = BeautifulSoup(page.text)

prdtBloc = soup.find_all("div", class_='prdtBloc')


prdtDATA = {}
for prdt in prdtBloc:
    prdt = {}
    prdt['name'] = prdt.find("div", class_='prdtBTit').get_ext()
    prdt['url'] = prdt.find("a").get('href')
