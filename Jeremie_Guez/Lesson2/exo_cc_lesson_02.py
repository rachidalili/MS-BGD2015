# coding: utf8

import requests
from bs4 import BeautifulSoup



def extractIntFromText(text):
  return int(text.replace(u'\xa0', u''))

def extractGenericLike(soup,classname):
  like_button = soup.findAll("button", { "class" : classname })[0]
  like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
  like_count = extractIntFromText(like_count_str)
  return like_count

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractMetricsFromUrl(url):

  soup = getSoupFromUrl(url)
  #GEt the view count
  view_count_str = soup.findAll("div", { "class" : "watch-view-count" })[0].text
  view_count = extractIntFromText(view_count_str)

  #GEt the like count
  like_count = extractGenericLike(soup,"like-button-renderer-like-button")
  #GEt the like count
  dislike_count = extractGenericLike(soup,"like-button-renderer-dislike-button")

  metrics = {}
  metrics['title'] = soup.title.text
  metrics['view_count'] = view_count
  #metrics['like_count'] = like_count
  #metrics['dislike_count'] = dislike_count
  metrics['indicator'] = 1000.* (like_count - dislike_count) / view_count

  print '===='
  print 'Handling ' , soup.title.text
  print 'The like count is', like_count, ' and dislike ', dislike_count
  print 'Popularity indicator is ' , metrics['indicator']
  print '===='
  return metrics


#extractMetricsFromUrl('https://www.youtube.com/watch?v=B3eAMGXFw1o')
#extractMetricsFromUrl('https://www.youtube.com/watch?v=Ao8cGLIMtvg')
#extractMetricsFromUrl('https://www.youtube.com/watch?v=lWA2pjMjpBs')

MAX_PAGE = 1
def getAllMetricsForArtist(artist):
  all_metrics = []
  for i in range(0,MAX_PAGE):
    url = 'https://www.youtube.com/results?search_query='+artist+'&page='+str(i)
    soup = getSoupFromUrl(url)
    tile_links = soup.findAll("a", { "class" : "yt-uix-tile-link" }) #PAS COMPRIS
    for tile_link in tile_links:
        if 'watch' in tile_link['href']:
          url = 'https://www.youtube.com' + tile_link['href']
          metrics_for_url = extractMetricsFromUrl(url)
          all_metrics.append(metrics_for_url)
  return all_metrics


rihanna = getAllMetricsForArtist('rihanna')



