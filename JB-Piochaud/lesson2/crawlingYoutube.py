# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import requests
from bs4 import BeautifulSoup

url = "https://www.youtube.com/watch?v=kt0g4dWxEBo"

def getSoupFromUrl(url):
  """Execute la requête"""
  request = requests.get(url)
  """et parse le résultat de la requette"""
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
def writeSoup(file, soup):
    nameFile = open(file, "w")
    nameFile.write(soup.prettify())
    nameFile.close()
    
def writeElement(file, element):
    nameFile = open(file, "w")
    for i in range(0, len(element)):
        nameFile.write(element[i])
    nameFile.close()
    
def removeEncodingFromElement(element):
    elementList = []    
    for i in range(0, len(element)):
        elementList.append(int(element[i].replace(u'\xa0', u'')))
    return elementList
    
def getElement(soup, element, classname):
    elementList = []    
    el = soup.findAll(element, { "class" : classname })
    for i in el:
        elementList.append(i.text)
    return elementList

def main():
    soup = getSoupFromUrl(url)
    likeButton = getElement(soup, "button", "like-button-renderer-like-button")
    print(likeButton)
    likeButton = removeEncodingFromElement(likeButton)
    print(likeButton)
    dislikeButton = getElement(soup, "button", "like-button-renderer-dislike-button")
    print(dislikeButton)
    dislikeButton = removeEncodingFromElement(dislikeButton)
    print(dislikeButton)
    titleSong = getElement(soup, "span", "watch-title")
    print(titleSong)
    #writeSoup("soup1.txt", soup)
    #print(LikeButton[1])
    #writeElement("element1.txt", LikeButton)
