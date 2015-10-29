import urllib2  #python 2
from bs4 import BeautifulSoup
import re

data_table = []

url = "http://www.cdiscount.com/search/10/acer+aspire.html"
data = []
page = 0


html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
entries = soup.findAll('div', {'class': 'prdtBloc'})
for entry in entries:
    data_point = {}
    data_point['url'] = entry.find('a').get('href')
    data_point['title'] = entry.find('div', {'class': 'prdtBTit'}).get_text()
    data_point['image_url'] = entry.find('ul', {'class': 'prdtBPCar'}).find('img')['src']
    old_price = entry.find('div', {'class': 'prdtPrSt'})
    if old_price is not None and len(old_price.get_text().strip()) > 0:
        print (old_price.get_text())
        data_point['old_price'] = float(re.sub(r'\D', '', old_price.get_text().strip()))/100
    price = entry.find('span', {'class': 'price'}).get_text()
    data_point['price'] = float(re.sub(r'\D', '', price))/100
    data.append(data_point)

print (data)
