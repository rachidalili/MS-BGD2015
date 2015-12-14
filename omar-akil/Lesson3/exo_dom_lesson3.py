__author__ = 'omakil'


import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

cd_url = 'http://www.cdiscount.com/search/10/acer+aspire.html#_his_'
def getAllDataFromPage(url) :
    data = []
    all_data = []
    list_title = []
    list_img = []
    list_price = []
    img = []
    price = []
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
        data.append(list_title[i].encode('ascii', 'ignore').decode('ascii'))
        data.append(list_price[i].encode('ascii', 'ignore').decode('ascii'))
        data.append(list_img[i].encode('ascii', 'ignore').decode('ascii'))
        all_data.append(data)
    return all_data

all_data = getAllDataFromPage(cd_url)
print(all_data)




