import requests
from bs4 import BeautifulSoup


def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def FromTestToInt(txt):
    return int(txt.replace(u'\u20ac', u' ').replace(' ', ''))


def FromTextToTextWithPlus(txt):
    return txt.replace(' ', '+')

# for year in range(firstYear,LastYear+1):


def GetInfo(NameProduct):
    url = 'http://www.cdiscount.com/search/10/' + NameProduct + '.html#_his_'
    print(url)
    soup = GetSoupFromUrl(url)
    tile = soup.findAll("div", {"class": "prdtBloc"})
    for tiles_links in tile:
        title = tiles_links.findAll("div", {"class": "prdtBTit"})[0].text
        print 'title ', title
        oldPrice = tiles_links.find("div", {"class": "prdtPrSt"})[0].text
        if oldPrice is not None :
            print 'oldPrice ', oldPrice
        newPrice = tiles_links.findAll("span", {"class": "price"})[0].text
        print 'newPrice ', newPrice
        Des = tiles_links.findAll("p", {"class": "prdtBDesc"})[0].text
        print 'Description ', Des

NameProduct = 'acer aspire'
NameInForm = FromTextToTextWithPlus(NameProduct)
# print NameInForm
GetInfo(NameInForm)