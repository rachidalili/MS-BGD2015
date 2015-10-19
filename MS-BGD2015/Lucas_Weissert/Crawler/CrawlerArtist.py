import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  	#Execute q request
  	request = requests.get(url)
  	#parse the restult of the request
	soup = BeautifulSoup(request.text, 'html.parser')
  	return soup


def appendNameArtist(name):
  return name.replace(u' ', u'+')


#On passe en parametre une liste d artiste et on la retourne
def getArtists(artists, soup):
	# On recupere les articles contenant le nom de l artiste
	articles = soup.findAll("article", {"class":"masonry-brick"})
	for article in articles:
		#On recupere le nom de l'artiste.
		# [0] nous donne le lien de redirection, [1] le nom de l artiste
		artist = article.findAll("a")[1].text
		artist = appendNameArtist(artist)
		artists.append(artist)
	return artists



MAX_PAGE = 5
def getAllArtistsFromTop100(artists):
	for i in range(0, MAX_PAGE):
		url = "http://www.billboard.com/artists/top-100?page="+str(i)
		soup = getSoupFromUrl(url)
		getArtists(artists, soup)
	return artists

# artists = []
# getAllArtistsFromTop100()
#Affiche la liste des artistes
# print artists
#Verification d obtenir le top 100
# print len(artists)
# print artists[0]
