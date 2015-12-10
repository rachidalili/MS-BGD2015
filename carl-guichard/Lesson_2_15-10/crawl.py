# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def getSoupFromUrl(youtube_url):
	request = requests.get(youtube_url)
	soup = BeautifulSoup(request.text, 'html.parser')
	return soup

def getLinksFromSearch(soup):
	# creation du tableau de sorti avec tous les liens
	links = []
	tile_links = soup.findAll('a', { "class" : "yt-ui-ellipsis-2" })
	for tileLink in tile_links:
		if 'watch' in tileLink['href']:
			links.append('https://www.youtube.com' + tileLink['href'])

	return links

def getUrlFromLinks(videoLinks):
	urlLinks = []
	i = 0
	while i < len(videoLinks):
		urlLinks.append('https://www.youtube.com' + videoLinks[i])
		print urlLinks[i]
		i += 1

	return urlLinks

def extractAppreciation(videoSoup, button):
	tile_Appreciation = videoSoup.findAll("button", { "class" : button })[0]
	tile_Appreciation = tile_Appreciation.findAll("span", { "class" : "yt-uix-button-content" })[0].text
	tile_Appreciation = int(tile_Appreciation.replace(u'\xa0', u''))
	return tile_Appreciation

def getInfoFromLinks(videoLinks):

	infoVideo = []

	for videoLink in videoLinks:
		videoSoup = getSoupFromUrl(videoLink)
		#name number
		tile_name = videoSoup.title.text
		#viewed number 
		tile_viewed = videoSoup.findAll("div", { "class" : "watch-view-count" })[0].text
		viewed = int(tile_viewed.replace(u'\xa0', u''))
		# like and dislike
		tile_like = extractAppreciation(videoSoup, "like-button-renderer-like-button" )
		tile_dislike = extractAppreciation(videoSoup, "like-button-renderer-dislike-button" )
		#algo
		tile_rank = 1000*(tile_like - tile_dislike)/viewed
		#append
		infoVideo.append([tile_name, viewed, tile_like, tile_dislike, tile_rank])
	return infoVideo
	
def extractArtistInfo(artiste):
	#determination du nombre de page étudié
	maxPage = 2
	#les metrics
	allMetrics = []
	#bouvle sur le nombre de page
	for i = 1 to maxPage:
		youtube_url = 'https://www.youtube.com/results?search_query=' + artiste + '&page=' + i
		#recupération du code html de la page youtube pour chaque chanson de l'artiste selectionné
		soup = getSoupFromUrl(youtube_url)
		#récupération des liens de toutes les vidéos de la page et mise en forme des liens
		videoLinks = getLinksFromSearch(soup)
		#urlLinks = getUrlFromLinks(videoLinks)
		#récuération des vues like et dislike des vidéos de la page
		artistInformation = getInfoFromLinks(videoLinks)
		allMetrics.append(artistInformation)

### main ###

#choix de l'artiste
# possibilité de faire un tableau d'artiste
artiste = 'mattafix'
extractArtistInfo(artiste)
