# coding utf8
import requests
from bs4 import BeautifulSoup

#recuperer la page	
request=requests.get("https://www.youtube.com/watch?v=B3eAMGXFw1o")
#
soup = BeautifulSoup(request.text, 'html.parser')
view_count_str=soup.findAll("div",{"class":"watch-view-count"})
# view_count=int(view_count_str.replace(u''))
  #GEt the view count
#view_count_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
