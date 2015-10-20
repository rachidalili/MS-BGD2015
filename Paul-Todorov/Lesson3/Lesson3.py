# coding: utf8
from pylab import *
import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

url = 'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
soup = getSoupFromUrl(url)

tile = soup.findAll("div", { "class" : "prdtBloc" })
for tiles_links in tile:
    title = tiles_links.findAll("div", {"class":"prdtBTit"})[0].text
    print 'title', title
    desc = tiles_links.findAll("p", { "class" : 'prdtBDesc' })[0].text
    print 'description', desc
    Price = tiles_links.findAll("span",{ "class":"price"})[0].text
    print 'prix', Price
    print "=========="
    print "=========="
 
