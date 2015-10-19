__author__ = 'Mohamed Amine'


from bs4 import BeautifulSoup

import requests


def getLikes(mySoup):
    likes_count_button = mySoup.find_all("span", {"class" : "like-button-renderer"})
    likes_count = likes_count_button[0].find_all("span", {"class" : "yt-uix-button-content"})
    return likes_count

def getViews(mySoup):
    return mySoup.find_all("div", {"class" : "watch-view-count"})

def treat_link(myPage):
    #now on a youtube example
    youtube_page = requests.get(myPage)
    youtube_soup = BeautifulSoup(youtube_page.text, 'html.parser')

    print "view_count " + getViews(youtube_soup)[0].text
    print "likes count " + getLikes(youtube_soup)[0].text


# link_soup = youtube_soup.find_all("h3", {"class" : "yt-lockup-title"})
# video_soup = link_soup[1].find_all("a", {"class" : "yt-uix-sessionlink"})

treat_link("https://www.youtube.com/watch?v=BGpzGu9Yp6Y")

