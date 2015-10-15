# coding: utf8

import requests
from bs4 import BeautifulSoup




#Execute q request toward Youtube
request = requests.get('https://www.youtube.com/watch?v=e82VE8UtW8A')
#parse the restult of the request
soup = BeautifulSoup(request.text, 'html.parser')

#GEt the view count
view_count_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
view_count = int(view_count_str.replace(u'\xa0', u''))


#GEt the like count
like_button = soup.findAll("button", { "class" : "like-button-renderer-like-button" })[0]
like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
like_count = int(like_count_str.replace(u'\xa0', u''))

print 'Hello'
