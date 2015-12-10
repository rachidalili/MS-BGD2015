""""
@author: Cristiana
"""""

import requests
from bs4 import BeautifulSoup


def fromUrltoSoup( url):
    r = requests.get(url,  stream=True)
    return BeautifulSoup(r.text, 'html.parser')
    

def getmetrics( soup ):    
    sub_tile_links = soup.findAll("td", { "class" : "montantpetit G" })    
    print "Euros par hab (A): ",sub_tile_links[1].text
    print "** Moyenne strate (A): ",sub_tile_links[2].text
    print "Euros par hab (B): ",sub_tile_links[4].text
    print "** Moyenne strate (B): ",sub_tile_links[5].text
    print "Euros par hab (C): ",sub_tile_links[10].text
    print "** Moyenne strate (C): ",sub_tile_links[11].text
    print "Euros par hab (D): ",sub_tile_links[13].text
    print "** Moyenne strate (D): ",sub_tile_links[14].text


annees = ["2010", "2011", "2012","2013"]
for j in range(len(annees)):    
    print " \n\n"
    print "================== Recap annee", annees[j],'==================='
    url = u'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+annees[i]
    fromUrltoSoup( url) 
    getmetrics(fromUrltoSoup( url))
