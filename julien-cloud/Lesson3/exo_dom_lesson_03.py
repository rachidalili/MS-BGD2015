import urllib
import re
from bs4 import BeautifulSoup

url = "https://gist.github.com/paulmillr/2657075"

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

users = []

nodes = soup.find('article').find('table').findAll('a')
for node in nodes:
    user = node.get_text().encode('utf-8')
    if (len(user) > 0):
        users.append(user)

print users
