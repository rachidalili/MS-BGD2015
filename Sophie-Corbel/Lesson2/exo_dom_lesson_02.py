# coding: utf8

import requests
from bs4 import BeautifulSoup
import re

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getThreeAccountsFromLine(text,soup):
     tdText= soup.find('td', text = re.compile('.*'+text+'.*'))
     strateAmount = tdText.previous.previous
     residentAmount = strateAmount.previous.previous.previous
     totalAmount= residentAmount.previous.previous.previous
     return (strateAmount,residentAmount,totalAmount)

def printTable(table):
  print( "Année".ljust(5)," ".rjust(45),"Par strate".rjust(20),"Par resident".rjust(20),"Total".rjust(20))
  for row in table:
    print(str(row[0]).ljust(5),row[1].rjust(45),row[2].rjust(20),row[3].rjust(20),row[4].rjust(20))


def getParisAccount():
  for year in range(2010,2014):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year)
    soup = getSoupFromUrl(url)
    operationsCosts = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A","TOTAL DES CHARGES DE FONCTIONNEMENT = B","TOTAL DES RESSOURCES D'INVESTISSEMENT = C","TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
    table = []
    for cost in operationsCosts:
      (strate, resident,total)= getThreeAccountsFromLine(cost,soup)
      line=[]
      line.append(year)
      line.append(cost)
      line.append(strate)
      line.append(resident)
      line.append(total)
      table.append(line)
    printTable(table)



getParisAccount()

