import requests
from bs4 import BeautifulSoup


page = requests.get('http://www.cdiscount.com/search/10/acer+aspire.html#_his_')

soup = BeautifulSoup(page.text)

prdtBloc = soup.find_all("div", class_='prdtBloc')

for prdt in prdtBloc:

    href = prdt.find_all("a", href=True)

    print("href", href)

    prdtPage = requests.get(href)
    prdtSoup = BeautifulSoup(prdtPage.text)

    rdtSoup.prettify()
