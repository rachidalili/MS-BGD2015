
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
def extractIntFromText(text):
  return int(text.replace(u'\xa0', u''))
  
soup=getSoupFromUrl('http://www.cdiscount.com/search/10/acer+aspire.html')

metrics={}

for i in range (0,24):
    desc_product=soup.findAll("p", { "class" : "prdtBDesc" })[i].text
    title_product=soup.findAll("div", { "class" : "prdtBTit" })[i].text
    older_price=soup.findAll("div", { "class" : "prdtPrSt" })[i].text
    new_price=soup.findAll("span", { "class" : "price" })[i].text
    metrics['desc_product']=desc_product
    metrics['title_product']=title_product
    metrics['older_price']=older_price
    metrics['new_price']=new_price

print (metrics)