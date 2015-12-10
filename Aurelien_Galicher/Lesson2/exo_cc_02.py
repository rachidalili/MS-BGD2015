# coding: utf8
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

url= "http://www.cdiscount.com/search/10/acer+aspire.html#_his_"
soup= getSoupFromUrl(url)
#print (soup)



prdtBlo= soup.findAll("div", { "class" : "prdtBloc"})
prdtBloc= prdtBlo[0]
data_point= {}
data_point['url']= prdtBloc.find("a").get('href')
data_point['title']= prdtBloc.find("div", {"class" : "prdtBit"}).get_text()
data_point['image_url'] = prdtBloc('ul', {"class" : "prdtBPCar"}).find("img")["src"]
old_price = prdtBloc.find("div", {"class" : "prdtPrSt"})
if old_price is not None and len(old_price.get_text().strip()) > 0 :
	print  (old_price.get_text())

print (data_point)