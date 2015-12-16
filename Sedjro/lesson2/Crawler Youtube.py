# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:32:51 2015"""
#L' ordre des choses compte énormément, faut déclarer une variable avatn de lui
#appliquer une fonction
"""@author: bibiane
"""
import string
import requests
from bs4 import BeautifulSoup

#crummy.com/software/BeautifulSoup
#Encoding joelonsoftware/ artcicles/ unicode
#Execute rquests toward youtube

def getSoupfromurl(url):   #On entre une donnée donc l'url
    #Les espaces soulent beaucoup pour les def de fonctions
    req=requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')   #On la transforme en soup
    return soup #Il retourne le soup donc

def extractIntFromText(text):
    rep=int(text.replace(u'\xa0', u''))
    return rep 
    
def extractGenericLike(ici,classname):
  like_button = ici.findAll("button", { "class" : classname })[0]
  like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
  like_count = extractIntFromText(like_count_str)
  return like_count   
  
url= 'https://www.youtube.com/watch?v=RgKAFK5djSk'
ici=getSoupfromurl(url)  

ici.button
ici.find_all('button')
ici.button['class']
ici.find_all('div')

"ici.find_all.div['class']"

ici.findAll("button", { "class" })[0]
  
"""Le nombre de vues """  
view_count_str = ici.findAll("div", { "class" : "watch-view-count" })[0].text
#Sans rajouter le .text, il prend tout ce qu'il y a dans le div, y compris les balises
#"class" : "watch-view-count" permet de sortir ce qu'il y a dans class, et après watch-view-count
#dans class
#Sans le 0, il y a pas le .text? Aquoi sert aussi le zéro?
view_count_str

"""Remplacer les caracteres spéciaux"""
int(view_count_str.replace(u'\xa0', u''))
#oum=string.replace(view_count_str.replace(u'\xa0', u''), 'u', '') ne marche pas
#car on dirait qu'il ne reconnait pas u comme un string
#Je peux me passer du replace de  u'\xa0' par u''  et me contenter
#du replace('\xa0', '')
#Si on n'y applique pas l'integer il garde le u
  
view_count=int(view_count_str.replace('\xa0', ''))
#Pourquoi met il un warning? lol il est parti

view_compte = extractIntFromText(view_count_str) 

"""Nombre de j'aime """
like_button = ici.findAll("button", { "class" : "like-button-renderer-like-button" })[0]
#Pourquoi le 0
# Notre compteur de like est situé princpalement dans button
#On a pris le text après "like-button-renderer-like-button" Part 1

like_count_str = like_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
#Sachant que ce nombre est dans la balise span,on la cherche dans le like_button de taleur
#et on prend ce qui est situé après le "yt-uix-button-content" ¨Part 2 

like_count=extractIntFromText(like_count_str)
like_count

"""Nombre de j'aime pas """
dislike_button = ici.findAll("button", { "class" : "like-button-renderer-dislike-button" })[0]
#Le 0 permet de prendre en compte le premier button uniquement 
#Prendre comme paramètre du class la phrase pouvant réeellement etre personnelle
#à l'élément qu'on inspecte sinon elle rique d'etre commune à beaucoup d'éléments button
#et il va etre compliqué de pouvoir juste choisir la partie qui nous intéresse
dislike_count_str = dislike_button.findAll("span", { "class" : "yt-uix-button-content" })[0].text
dislike_count = extractIntFromText(dislike_count_str)
dislike_count

def extractMetricsFromUrl(url):
    ici = getSoupFromurl(url)
#On transforme l'url en langage python qu'on importe
    
#GEt the view count
view_count_str = ici.findAll("div", { "class" : "watch-view-count" })[0].text
view_count = extractIntFromText(view_count_str)

#GEt the like count
like_count = extractGenericLike(ici,"like-button-renderer-like-button")
#GEt the dislike count
dislike_count = extractGenericLike(ici,"like-button-renderer-dislike-button")

metrics = {}
metrics['title'] = ici.title.text
#metrics['view_count'] = view_count
#metrics['like_count'] = like_count
#metrics['dislike_count'] = dislike_count
metrics['indicator'] = 1000.* (like_count - dislike_count) / view_count

print '===='
print 'Handling ' , ici.title.text
print 'The like count is', like_count, ' and dislike ', dislike_count
print 'Popularity indicator is ' , metrics['indicator']
print '===='
return metrics
  
  
extractMetricsFromUrl ('https://www.youtube.com/watch?v=RgKAFK5djSk')
  
  
  
  
  
ici.findAll("button", { "class" : classname })[0]

view_count_fr = soup.findAll("div", { "class" : "watch-view-count"})[0].text

soup.title

