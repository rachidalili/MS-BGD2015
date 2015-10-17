# coding: utf8
import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.youtube.com/watch?v=B3eAMGXFw1o')
soup = BeautifulSoup(request.text, 'html.parser')
view_count_str = soup.findAll("div", {"class": "watch-view-count"})[0].text
view_count= int(view_count_str.replace('\xa0',''))