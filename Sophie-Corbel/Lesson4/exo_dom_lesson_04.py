# coding: utf8
import requests
from bs4 import BeautifulSoup
import operator
import pandas as pd
import re

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup


def searchToLinks(region,search):
    links = []
    url = baseUrl + region+"/?q="+search
    soup = getSoupFromUrl(url)

    for i, aTag in enumerate(soup.findAll('a')):
        href = aTag.get('href')
        if href:
            if linkRegex.match(href):
                links.append(href)
    return links

def getCarInfo(links):
    df = pd.DataFrame(columns=['version', 'année', 'km', 'prix', 'pro'])
    id=0
    for link in links:
        soup = getSoupFromUrl(link)
        title = soup.findAll("h1", { "id" : "ad_subject" })[0]
        m = re.match(r".*[Zz]o[eé] ([a-zA-Z]+)", title.text)
        if m != None:
            version= m.group(1).lower()
            spanAddPro = soup.findAll("span",{"class":"ad_pro"})
            if len(spanAddPro)>0 :
                ventePro=1
            else:
                ventePro=0
            price = soup.find("span",{"class":"price"})['content']
            div = soup.find("div",{"class":"lbcParams criterias"})
            table = div.findNext("table")
            year=""
            km=""
            for tr in table.findAll("tr"):
                td = tr.findNext("td")
                if bool(td.attrs) :
                    if td['itemprop']=='releaseDate':
                        year = td.text.trim()
                m = re.match(r"([0-9 ]+) KM",td.text)
                if  m != None :
                    km=m.group(1).replace(' ','')
            df = df.append({
            'version': version,
            'année': year,
            'km': km,
            'prix': price,
            'pro': ventePro
            }, ignore_index=True)
    return df



regions = ["ile_de_france"]
baseUrl= "http://www.leboncoin.fr/voitures/offres/"
linkRegex = re.compile("http://www.leboncoin.fr/voitures/([a-z0-9]+){8,12}\\.htm?.*$")
carName="Renault+Zoe"
for region in regions:
    links=searchToLinks(region,carName)
df=getCarInfo(links)
print(df)









