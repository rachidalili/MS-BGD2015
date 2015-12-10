# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 22:07:01 2015

@author: jean-baptiste

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def getSoupFromDynamicUrl(year):
    url_static = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
    url_dynamic = {'icom': '056', 'dep': '075', 'type': 'BPS',
              'param': '0', 'exercice': str(year)}
    request = requests.get(url_static, params = url_dynamic)
    soup = BeautifulSoup(request.text, 'html.parser')
    #print(request.text)
    return soup

def getTableFromSoup(soup):
    el = soup.findAll("table")
    return el[2]
    
def writeSoup(file, soup):
    nameFile = open(file, "w")
    nameFile.write(soup.prettify())
    nameFile.close()

def removeEncodingFromValues(TableOfValues):  
    for el in TableOfValues:
        el.replace(u'\xa0', u'')
    return TableOfValues

def getValuesFromTable(table):
    forRow = [8, 12, 20, 25]
    forCol = [1, 3]
    TableOfValues = [[0]*4]*2
    for i in range(0, len(forRow)):
        for j in range(0, len(forCol)):
            selectorRow = 'tr:nth-of-type(' + str(forRow[i]) + ') '
            selectorCol = 'td:nth-of-type(' + str(forCol[j]) + ')'
            selector = selectorRow + selectorCol
            TableOfValues[j][i] = table.select(selector)[0].text
            TableOfValues[j][i] = TableOfValues[j][i].replace(u'\xa0', u'')
    return TableOfValues
    
def displayValues(values):
    dataframe = pd.DataFrame(values, index=['Euros par habitant', 'Moyenne de la strate'],
                             columns=['A', 'B', 'C', 'D'])
    dataframe = dataframe.transpose()
    return dataframe
    

def main():   
    for year in range(2010, 2014):  
        soup = getSoupFromDynamicUrl(year)
        table =  getTableFromSoup(soup)
        values = getValuesFromTable(table)
        dfValues = displayValues(values)
        print("--------")
        print(year)
        print("--------")
        print(dfValues)
        
if __name__ == '__main__':
    main()  