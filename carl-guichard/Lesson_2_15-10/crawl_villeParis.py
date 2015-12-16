# coding: utf8

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text)
    return soup

def getDataFromSoup(soup, year):
    lines = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B", "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
    dataArray = []
    for line in lines:
        soup_first = soup.find("td", text=line)
        soup_second = soup_first.find_previous_siblings("td")

        # moyenne par strate
        moyenne_par_strate = soup_second[0].text
        moyenne_par_strate = moyenne_par_strate.replace(u'\xa0', u'')

        #euros pas habitant
        euros_par_habitant = soup_second[1].text
        euros_par_habitant = euros_par_habitant.replace(u'\xa0', u'')

        dataArray.append([year, line, euros_par_habitant, moyenne_par_strate])
    return dataArray


def miseEnForme(allResults):
    for i in range(4):
        print "============="
        print allResults[i][0][0]
        for j in range(4):
            print allResults[i][j][1]
            print "Euros par habitant :" + str(allResults[i][j][2])
            print "moyenne de la strate :" + str(allResults[i][j][3])
    return


# Main
baseUrl = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
years =[2010, 2011, 2012, 2013]
allResults =[]
for year in years:
    url = baseUrl + str(year)
    soup = getSoupFromUrl(url)
    dataArray = getDataFromSoup(soup, str(year))
    allResults.append(dataArray)
miseEnForme(allResults)



