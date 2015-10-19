# -- coding: utf-8 --
#^^^^ Keep this line if you plan to use french characters (even in comments)
#Comme exercice pour mardi prochain je vous demande de crawler le resultat des comptes de la ville
#  de Paris pour les exercices 2009 à 2013. Voici par exemple les comptes pour 2013 . Je vous
# demande de récupérer les données A,B,C et D sur les colonnes Euros par habitant et par strate.
#
#Pour le travail de crawling que je vous ai demandé vous aurez besoin de connaitre les selecteurs css.
#Notamment vous aurez besoin des selecteur nth-of-type .

#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
import requests
import pandas as pd
from bs4 import BeautifulSoup

def composePage(year):
    """
    returns the page for Paris accounts for the year passed as an argument.
    Arguments :
    year : integer comprised between 2000 and 2014
    """
    if year < 2000 | year > 2014:
        raise ValueError('Year must be comprised between 2000 and 2014!')

    params = {'icom': '056', 'dep': '075', 'type': 'BPS',
              'param': '0', 'exercice': str(year)}
    #Exception for 2009 
    if year <= 2009:
        params['icom'] = '101'
    url_base = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
    r = requests.get(url_base, params=params)
    return r.text


def textToInt(text):
    """converts text to integer, removing unreadable characters"""
    return text.replace(u'\xa0', '').replace(' ', '')


def findNumberInHTMLTable(row, col, table):
    """Finds the number associated to the arguments (row, col) in the table"""
    selector = 'tr:nth-of-type(' + str(row) + ') td:nth-of-type(' + str(col) + ')'
    return textToInt(table.select(selector)[0].text)

#Returns a table of 4x2 containing one column for Citizen and the other for Strate
def calculateResultsForYear(year):
    """Returns the results for a year"""
    soup = BeautifulSoup(composePage(year), 'html.parser')
    rowNumbers = [8, 12, 20, 25]
    colNumbers = [2, 3]
    return [[findNumberInHTMLTable(r, c, soup('table')[2]) for r in rowNumbers] for c in colNumbers]


def main():
    # Return a list containing an arithmetic progression of integers.
    # range(i, j) returns [i, i+1, i+2, ..., j-1];
    years = range(2009, 2014) #Will return till 2013
    resultsPerCitizen = pd.DataFrame(columns=years, index=['A-TOTAL DES PRODUITS DE FONCTIONNEMENT', 'B-TOTAL DES CHARGES DE FONCTIONNEMENT', 'C-TOTAL DES RESSOURCES D INVESTISSEMENT', 'D-TOTAL DES EMPLOIS D INVESTISSEMENT'])
    resultsPerStrate = pd.DataFrame(columns=years, index=['A-TOTAL DES PRODUITS DE FONCTIONNEMENT', 'B-TOTAL DES CHARGES DE FONCTIONNEMENT', 'C-TOTAL DES RESSOURCES D INVESTISSEMENT', 'D-TOTAL DES EMPLOIS D INVESTISSEMENT'])
    for y in years:
        res = calculateResultsForYear(y)
        #Load column by column
        resultsPerCitizen[y] = res[0]
        resultsPerStrate[y] = res[1]
    print('TOTALS par Habitant :')
    print('################################')
    print(resultsPerCitizen)
    print('TOTALS par Strate :')
    print('################################')
    print(resultsPerStrate)

if __name__ == '__main__':
    main()
