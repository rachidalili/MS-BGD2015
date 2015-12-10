import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import xlrd
def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def FromTestToInt(txt):
    return int(txt.replace(u'\u20ac', u' ').replace(' ', ''))


def FromTextToTextWithPlus(txt):
    return txt.replace(' ', '+')

cheminCSV = '/Users/williambenhaim/ProjetMSBigData/MS-BGD2015/Lessons-Exercices/exo.xls'
book2=pd.read_excel(cheminCSV,skiprows=11, sheetname=0)

book2[['country', 'target']]=pd.DataFrame([x.split('_')[1:3] for x in book2['campaign']])

