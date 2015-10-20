__author__ = 'khalil'

import urllib2
from bs4 import BeautifulSoup
page = urllib2.urlopen('https://www.youtube.com/watch?v=Ao8cGLIMtvg').read()
soup = BeautifulSoup(page)

#print soup.find_all('a')
print soup.find("button", {"class": "like-button-renderer-like-button"})
button = soup.find("button", {"class": "like-button-renderer-like-button"})
print button.find("span", {"class": "yt-uix-button-content"}).next
print soup.find("div", {"class": "watch-view-count"}).next


