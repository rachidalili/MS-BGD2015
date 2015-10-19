# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:37:07 2015

@author: Carl
"""

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.title)


request = requests.get('https://www.youtube.com/watch?v=e82VE8UtW8A')
soup = BeautifulSoup(request.text, 'html.parser')
print(soup)
# view_count_str = soup.findALL("div", )