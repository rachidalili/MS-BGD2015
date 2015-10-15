import requests
from bs4 import BeautifulSoup


def extractIntFromText(text):
	return int(text.replace(u'\xa0',u''))

def extractGenericLike(classname):
	like_button = soup.findAll("button",{"class" : classname})[0]
	like_count_str = like_button.findAll("span",{"class" : "yt-uix-button-content"})[0].text
	like_count = extractIntFromText(like_count_str)
	return like_count

def getSoupFromUrl(url):
	sou

def extractMetricsFromUrl(url):
    #execute q request toward youtube
	request = requests.get(url)
	#parse the result of the request
	soup = BeautifulSoup(request.text,'html.parser')



view_count_str = soup.findAll("div",{ "class" : "watch-view-count" })[0].text
view_count = extractIntFromText(view_count_str)


#get the like button
like_count = extractGenericLike("like-button-renderer-like-button")

#get the dislike button
dislike_count = extractGenericLike("like-button-renderer-dislike-button")


metrics = {}
metrics['view_count'] = view_count
metrics['like_count'] = like_count
metrics['dislike_count'] = dislike_count
metrics['indicator'] = 1.* (like_count - dislike_count)/ view_count

print '===='
print 'Handling',soup.title.text
print "the like count is", metrics['view_count'], ' and dislike', metrics['dislike_count']
print "popularity indicator is", metrics['indicator']
