__author__ = 'largo'

import urllib
import requests
from bs4 import BeautifulSoup

    thisurl = "http://www.youtube.com/watch?v=B3eAMGXFw1o"
#get html
request =requests.get(thisurl)
#parse doc
soup = BeautifulSoup(request.text, 'html.parser')

view_count_str = soup.findAll("div",{"class":"watch-view-count"})[0].text
view_count = int(view_count_str.replace(u'\xa0', u' '))

print(view_count)

urlText = []

#Define HTML Parser


#lParser.feed(urllib.urlopen(thisurl).read())
#lParser.close()
#for item in urlText:
#    print item
print("hi")