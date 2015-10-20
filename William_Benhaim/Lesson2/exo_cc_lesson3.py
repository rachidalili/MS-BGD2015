import requests
from bs4 import BeautifulSoup

def GetSoupFromUrl(url):
	request=requests.get(url)
	return BeautifulSoup(request.text, 'html.parser')
def FromTestToInt(txt):
	return int(txt.replace(u'\u20ac',u' ').replace(' ',''))


#for year in range(firstYear,LastYear+1):
url='http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
soup = GetSoupFromUrl(url)
tile = soup.findAll("div", { "class" : "prdtBloc" })
for tiles_links in tile:
	title=tiles_links.findAll("div",{"class":"prdtBTit"})[0].text
	print 'title ',title
	# oldPrice=tiles_links.find("div",{"class":"prdtPrSt"})[0].text
	# if oldPrice is not None and len(oldPrice)>0:
	# 	oldPrice=tiles_links.findAll("div",{"class":"prdtPrSt"})[0].text
	# 	print 'oldPrice ',oldPrice
	newPrice=tiles_links.findAll("span",{"class":"price"})[0].text
	print 'newPrice ',newPrice
	Des=tiles_links.findAll("p",{"class":"prdtBDesc"})[0].text
	print 'Des ',Des
