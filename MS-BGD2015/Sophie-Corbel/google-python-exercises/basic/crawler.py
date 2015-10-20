__author__ = 'sophi'

import requests
from bs4 import BeautifulSoup
"""
"""
r =requests.get("https://www.youtube.com/watch?v=B3eAMGXFw1o")
soup = BeautifulSoup(r.text,'html.parser')
view_count=soup.find_all("div",{"class":"watch-view-count"})[0].text


