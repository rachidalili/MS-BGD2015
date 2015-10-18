import requests
import pandas as pd
from bs4 import BeautifulSoup

def getPage(year):
    """
    return the page for Paris accounts for the year passed as an argument.
    Arguments :
    year : integer comprised between 2000 and 2014
    """
    if year < 2000 | year > 2014:
        raise ValueError('Year must be comprised between 2000 and 2014!')

    params = {'icom': '056', 'dep': '075', 'type': 'BPS',
              'param': '0', 'exercice': str(year)}
    if year <= 2009:
        params['icom'] = '101'
    url_base = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
    r = requests.get(url_base, params=params)
    return r.text


def isRowUseful(usefulText, row):
    """
    Check if one cell content of the row contains a text of argument usefulText
    Arguments:
    usefulText: list of useful text
    row: a list of soup tags
    """
    seq = [t in c.text for c in row('td') for t in usefulText]
    return True in seq

    
def convertToInt(text):
    """converts text to integer, removing unreadable characters"""
    return text.replace(u'\xa0', '').replace(' ', '') 


def findNumber(row, col, table):
    """Finds the number associated to the arguments (row, col) in the table"""
    selector = 'tr:nth-of-type(' + str(row) + ') td:nth-of-type(' + str(col) + ')'
    return convertToInt(table.select(selector)[0].text)


def resultsByYear(year):
    """Returns the results for a year"""
    soup = BeautifulSoup(getPage(year), 'html.parser')
    rowNumbers = [8, 12, 20, 25]
    colNumbers = [2, 3]
    return [[findNumber(r, c, soup('table')[2]) for r in rowNumbers] for c in colNumbers]
    

def main():
    years = range(2009, 2014)
    resultsPerCitizen = pd.DataFrame(columns=years, index=['A', 'B', 'C', 'D'])
    resultsPerStrate = pd.DataFrame(columns=years, index=['A', 'B', 'C', 'D'])
    for y in years:
        res = resultsByYear(y)
        resultsPerCitizen[y] = res[0]
        resultsPerStrate[y] = res[1]
    print('Results by Citizens :')
    print(resultsPerCitizen)
    print('Resutls by Strate :')
    print(resultsPerStrate)

main()
