
#################################################""
# imports communs 


import requests
from bs4 import BeautifulSoup


##################################################""
# fonctions communes 

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getData():

	return data


###################################################



def getAllDataFromPage() :
	#list format return is A list of lists with data of A, B, C, D
	data = []
	all_data = []
	list_title = []
	list_img = []
	list_price = []
	img = []
	price = []
	url = 'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
	soup = getSoupFromUrl(url)
	titles = soup.select(".prdtBTit")
	imgs = soup.select(".prdtBImg")
	prices = soup.select(".price")
	i=0
	print("-----------")
	for title in titles:
		list_title.append(title.text)
	for img in imgs:
		list_img.append(img.text)
	for price in prices:
		list_price.append(price.text)
	for i in range (0,10):
		data.append(list_title[i])
		data.append(list_price[i])
		data.append(list_img[i])
		all_data.append(data)
	return all_data


##############################################
#code execution
##############################################
all_data = getAllDataFromPage()
print(all_data)


