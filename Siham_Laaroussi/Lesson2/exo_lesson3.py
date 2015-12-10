__author__ = 'Siham_laaroussi'

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def getusers(soup):
