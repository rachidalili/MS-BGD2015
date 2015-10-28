__author__ = 'Siham_laaroussi'

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

soup=getSoupFromUrl('https://www.reddit.com/#')
soup.findAll("a",{"class":"title may-blank "})
