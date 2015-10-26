import requests
from bs4 import BeautifulSoup
import json


def crawling():

    page = requests.get('https://gist.github.com/paulmillr/2657075')
    soup = BeautifulSoup(page.text)

    print(soup('table'))

    for i in range(1,257):
        selector = 'tr:nth-of-type(' + str(i) + ') td:nth-of-type(2)'

        text = soup('table').select(selector)[0].text

        print(text)

    href = soup.select("th > td")

    print(href)

    #for link in href:
    #        print(link['href'])


    #cells = soup.select("th", scope_="#1")

    #name = soup.select("# > td > ol > li > span > strong > a")


    #print(cells)




def API():
    answer = requests.get("https://api.github.com/search/code?q={query}{&page,per_page,sort,order}")

    answer = json.load(answer)

    print(answer)
