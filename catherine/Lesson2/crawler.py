import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.youtube.com/watch?v=-N_SqtFerjg")
print(r.status_code)
print(r.headers)

soup = BeautifulSoup(r.text, 'html.parser')
view_count = soup.find_all("div", {"class": "watch-view-count"})[0].text
view_count = int(view_count.replace("\xa0", ""))
print(view_count)