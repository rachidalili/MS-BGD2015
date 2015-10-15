# coding: utf8

import requests
from bs4 import BeautifulSoup




#Execute q request toward Youtube
request = requests.get('https://www.youtube.com/watch?v=e82VE8UtW8A')
#parse the restult of the request
soup = BeautifulSoup(request.text, 'html.parser')
view_count_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
view_count = int(view_count_str.replace(u'\xa0', u''))



print 'Hello'
