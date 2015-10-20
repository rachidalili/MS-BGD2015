import requests
from bs4 import BeautifulSoup

print('ok')

#execute the request toward Youtube
request = requests.get('https://www.youtube.com/watch?v=lWA2pjMjpBs')
#parse the result of the request
soup = BeautifulSoup(request.text, 'html.parser')

viewcount_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
viewcount = int(viewcount_str.replace(' ',''))

print(viewcount)
print(soup.title)

