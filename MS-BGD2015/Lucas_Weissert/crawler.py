from bs4 import BeautifulSoup
import urllib
import urlparse
import requests
from collections import Counter
import pandas
import matplotlib.pyplot as plt

URL = 'https://www.youtube.com'
chanteurs = []
titres = []
comptes_youtube = []
vues = []
dates = []

URLS = [URL] # Stack des urls a scraper
visited = [URL] # Historique des urls scrapes

while len(URLS) > 0:
	try:
		htmltext = urllib.urlopen(URLS[0]).read()
	except:
		print URLS[0]
	soup = BeautifulSoup(htmltext)

	URLS.pop(0)

	for tag in soup.findAll('a', href=True):
		pass

r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')
#print soup

for node in soup.findAll("div", {"class":"yt-lockup-content"}):
		informations = node.findAll(['a', 'li'])
		print informations[0].text.encode('utf-8').split(' - ')
		print informations[1].text.encode('utf-8')
		print informations[2].text.encode('utf-8')
		print informations[3].text.encode('utf-8')
		

		chanteur_titre = informations[0].text.encode('utf-8').split(' - ')
		if len(chanteur_titre) < 2:
			continue
		print ('taille ' + str(len(chanteur_titre)))
		chanteurs.append(chanteur_titre[0])
		titres.append(chanteur_titre[1])
		comptes_youtube.append(informations[1].text.encode('utf-8'))
		vues.append(informations[2].text.encode('utf-8'))
		dates.append(informations[3].text.encode('utf-8'))

		# for informations in node.findAll(['a', 'li']):
		# 	print informations.text.encode('utf-8')
		print '_________'

print chanteurs
print Counter(chanteurs)

df = pandas.DataFrame.from_dict(Counter(chanteurs), orient='index')
df.plot(kind='bar')
plt.show()
# df.plot(title='Title Here')
