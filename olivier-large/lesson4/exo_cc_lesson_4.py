import requests
import pandas as pd
from bs4 import BeautifulSoup


def readCsv(path):
	tab = pd.read_csv(path).values;
	return tab


all_data = readCsv('villes.csv')

origins =

print(all_data)


