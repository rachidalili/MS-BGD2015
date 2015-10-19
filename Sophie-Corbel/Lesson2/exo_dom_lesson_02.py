# coding: utf8

import requests
from bs4 import BeautifulSoup
import re

class ParisAccount (object):
    def __init__(self,lineMap,rowTuple):
      self.lineMap = dict(lineMap)
      self.rowTuple = tuple(rowTuple)
      self.table = []

    def __str__(self):
        text = "Année".ljust(5)+" ".rjust(45)+"Total".rjust(20)+"Par resident".rjust(20)+"Par strate".rjust(20)+"\n"
        sep=""
        for row in self.table:
            text = text + sep + str(row[0]).ljust(5)+row[1].rjust(45)+row[2].rjust(20)+row[3].rjust(20)+row[4].rjust(20)
            sep="\n"
        return text

    def getCssTd(self,colNum):
      return 'td:nth-of-type('+str(colNum)+')'


    def setTable(self,soup,year):
      for rowKey in sorted(self.lineMap.keys()):
        rowNum = self.lineMap[rowKey]
        trSelected='tr:nth-of-type('+str(rowNum)+')'
        line=[]
        line.append(year)
        line.append(rowKey)
        totalAmount = soup.select(trSelected+ ' > '+self.getCssTd(self.rowTuple[0]))[0].text
        residentAmount = soup.select(trSelected+ ' > '+self.getCssTd(self.rowTuple[1]))[0].text
        strateAmount = soup.select(trSelected+ ' > '+self.getCssTd(self.rowTuple[2]))[0].text
        line.append(totalAmount)
        line.append(residentAmount)
        line.append(strateAmount)
        self.table.append(line)




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


def getParisAccounts():
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


def getParisAccountsoop():
    for year in range(2010,2014):
        url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year)
        soup = getSoupFromUrl(url)
        operationsCosts = {"A = TOTAL DES PRODUITS DE FONCTIONNEMENT": 10,"B = TOTAL DES CHARGES DE FONCTIONNEMENT": 14,"C = TOTAL DES RESSOURCES D'INVESTISSEMENT":22,"D = TOTAL DES EMPLOIS D'INVESTISSEMENT":27}
        amountsPositions =(1,2,3)
        pAccounts = ParisAccount(operationsCosts,amountsPositions)
        pAccounts.setTable(soup,year)
        print(pAccounts)


getParisAccounts()
print("Version oop ---------------------------------------------------------------------------------------------------------------------")
getParisAccountsoop()

