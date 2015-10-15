# coding: utf8

import requests
from bs4 import BeautifulSoup



def extractIntFromText(text):
  return int(text.replace(u'\xa0', u''))

def extractGenericLike(classname):
  like_button = soup.findAll("button", { "class" : classname })[0]
  like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
  like_count = extractIntFromText(like_count_str)
  return like_count

#Execute q request toward Youtube
request = requests.get('https://www.youtube.com/watch?v=e82VE8UtW8A')
#parse the restult of the request
soup = BeautifulSoup(request.text, 'html.parser')

#GEt the view count
view_count_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
view_count = extractIntFromText(view_count_str)

#GEt the like count
like_count = extractGenericLike("like-button-renderer-like-button")
#GEt the like count
dislike_count = extractGenericLike("like-button-renderer-dislike-button")

print 'Hello'
