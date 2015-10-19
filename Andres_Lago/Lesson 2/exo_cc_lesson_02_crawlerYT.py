# coding: utf-8

import urllib
import re
from bs4 import BeautifulSoup

urls = [{'artist': 'rihanna',
        'url_index': 'https://www.youtube.com/channel/UCvWtix2TtWGe9kffqnwdaMw/videos'},
        {'artist': 'beyonce',
        'url_index': 'https://www.youtube.com/channel/UCoPQ_TWm8JZ5nJv4a5BzSWA/videos'}]

for url in urls:
    htmlindex = urllib.urlopen(url['url_index']).read()
    soupindex = BeautifulSoup(htmlindex, 'lxml')
    for node in soupindex.findAll('div', {"class": "yt-lockup-content"}):
        link = node.find('a')
        htmlvideo = urllib.urlopen('https://www.youtube.com' + link['href']).read()
        soupvideo = BeautifulSoup(htmlvideo, 'lxml')
        views = soupvideo.find('div', {'class': 'watch-view-count'}).text
        views = int(re.sub(r'\D', '', views))
        likes = soupvideo.find('button', {'class': 'like-button-renderer-like-button'}).text
        likes = int(re.sub(r'\D', '', likes))
        dislikes = soupvideo.find('button', {'class': 'like-button-renderer-dislike-button'}).text
        dislikes = int(re.sub(r'\D', '', dislikes))
        indicator = (likes - dislikes) / float(views) * 1000

        print(url['artist'], soupvideo.title, views, likes, dislikes, indicator)
