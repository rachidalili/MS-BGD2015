from lxml import html
from bs4 import BeautifulSoup
import requests


page = requests.get('http://stackoverflow.com/questions/3207418/crawler-vs-scraper')

soup = BeautifulSoup(page.text)


posts = soup.find_all("div", class_="post-text")

posts_list = []
for post in posts:

    paragraphs = post.find_all('p')

    text = ""

    for p in paragraphs:
        text = text + p.get_text().replace('\n', ' ').lower().strip()

    posts_list.append(text)

for post in posts_list:
    print(post)
    print()
