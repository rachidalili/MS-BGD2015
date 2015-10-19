__author__ = 'Mohamed Amine'

from bs4 import BeautifulSoup

import requests


def getTagMatches(mySoup, tagName, documentSpec):
    return mySoup.find_all(tagName, documentSpec)

def parse_report_page(myPage):
    # now on a youtube example
    paris_exercise__page = requests.get(myPage)
    paris_soup = BeautifulSoup(paris_exercise__page.text, 'html.parser')

    print "C_per_Strate " + getTagMatches(paris_soup, "tbody", None)[0].text


# link_soup = youtube_soup.find_all("h3", {"class" : "yt-lockup-title"})
# video_soup = link_soup[1].find_all("a", {"class" : "yt-uix-sessionlink"})

parse_report_page("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013")

