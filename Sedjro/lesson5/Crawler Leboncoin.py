# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 21:13:31 2015

@author: bibiane
"""

import re
import string
import requests
from bs4 import BeautifulSoup
import time
import os

def getSoupfromurl(url):   
    req=requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup 

def extractIntFromText(text):
    rep=text.replace(u'\xa0', u'').replace(u'\u20ac', u'').replace(' ','')
    return rep

url= 'http://www.leboncoin.fr/voitures/878093374.htm?ca=12_s'
infos= getSoupfromurl(url)

def getPrice(url):
    infos= getSoupfromurl(url)
    Prix= infos.findAll("span", {"class" : "price"})[0].text
    return Prix
dob=getPrice(url)
extractIntFromText(dob)

KmEssai= infos.findAll("tr")

""" Utiliser le nth-of-type se fait avec le select pas avec le findAll """
""" On peut chercher une balise dans le nth-of-type avec le signe > """

def getKm(url):
    infos= getSoupfromurl(url)
    Km = infos.select('tr:nth-of-type(7) > td')[0].text.replace(u' ', '')
    return Km
    
getKm(url)

def getyear(url):
    infos= getSoupfromurl(url)
    Annee = int(infos.findAll("td", {"itemprop" : "releaseDate"})[0].text.replace(u'\n', '').replace(' ', ''))
    return Annee


def getphone(url):
    infos= getSoupfromurl(url)
    TelEssai = infos.select('div[class="AdviewContent"] > div[class="content"]')
    description = TelEssai[0].text.replace('\n','').strip()
    #TelEssai = infos.select('div[class="AdviewContent"] > div[class="content"]')
    #TelEssai = infos.find('div', {'itemprop': 'description'})
    expression = r"0[0-9]([ .-/]?[0-9]{2}){4}"
    #Il est très important de rajouter la description dans un str, vu qu'on recherche un string
    #sinon erreur du type expected string or buffer
    Telephone = re.search(expression,str(description))
    if Telephone:
        Telephone=Telephone.group() #Comprendre le group
        #Telephone = re.sub(r'\D', "", phone)
    else: Telephone='NA'
    return Telephone



def typevendeur(url):
    infos= getSoupfromurl(url)
    Type_Vendeur= infos.findAll("span", {"class" : "ad_pro"})[0].text
    #Ma manière de gérer une fonction like in python
    if 'Pro' in Type_Vendeur :
        Type_Vendeur = 'Pro'
    else: Type_Vendeur = 'Particulier'
    #return outside function, regarder la position dans le return
    return Type_Vendeur


#def typeversion(url):
   # infos= getSoupfromurl(url)
    #Version = infos.findAll("div", {"itemprop" : "description"})[0].text
    # version_fin = string.lowercase(Version) Savoir utiliser le lowercase
    #rep= r"([A-Za-z0-9-]+)"
    # version_fin= re.search(rep, str(Version))
    #version_fin=version_fin.group()
    #version_fin = re.compile(rep)
    #version_fin = version_fin.findall(Version)
    #if 'Zen' in version_fin:
        #version_fin = 'Zen'
        #if 'life' in version_fin:
            #version_fin = 'Life'
            #if 'Intens' in version_fin:
                #version_fin ='Intens'
    #return version_fin


#pattern = r"([A-Za-z0-9-]+)"
#regex_email = re.compile(pattern)
#version_fin = regex_email.findall(Version)
#if regex_email.findall('zen') in Version:
        #version_fin = 'Zen'
        #if regex_email.findall('life') in Version:
            #Version = 'Life'
            #if regex_email.findall('Intens') in Version:
                #Version ='Intens'

"""1ere alternative"""
def getversion(url) :
    infos= getSoupfromurl(url)
    Version = infos.findAll("div", {"itemprop" : "description"})[0].text
    regex_version = re.compile(r'(intens|life|zen)', re.IGNORECASE)
#On cherche les regex Intens/zen/life dans notre sujet Version
    version = regex_version.search(Version)
    if version : 
        version = version.groups()[0].lower()
    #Regarder l'alignement du else avec le if
    else: version = 'none'
    return str(version)
getversion(url)
   
"""2nd alternative"""
#def getversion(url)
#rexp = re.compile(r'(intens|life|zen)', re.IGNORECASE)
#Version = infos.findAll("div", {"itemprop" : "description"})[0].text
#return rexp.search(Version).group().lower() if rexp.search(title) is not None else ''
        
def getinfos(url) :
    #Initialiser le tableau dans lequel on aura les infos
    Lesinfos=[]
    infos= getSoupfromurl(url)
    
    Version = infos.findAll("div", {"itemprop" : "description"})[0].text
    regex_version = re.compile(r'(intens|life|zen)', re.IGNORECASE)
    version = regex_version.search(Version)
    if version : 
        version = version.groups()[0].lower()
    else: version = 'none'
    Lesinfos.append(str(version))
    Annee = int(infos.findAll("td", {"itemprop" : "releaseDate"})[0].text.replace(u'\n', '').replace(' ', ''))
    Lesinfos.append(Annee)
    
    Km = infos.select('tr:nth-of-type(7) > td')[0].text.replace(u' ', '')
    Lesinfos.append(Km)
    
    Type_Vendeur= infos.findAll("span", {"class" : "ad_pro"})[0].text
    if 'Pro' in Type_Vendeur :
        Type_Vendeur = 'Pro'
    else: Type_Vendeur = 'Particulier'
    Lesinfos.append(Type_Vendeur)
    
    Prix= infos.findAll("span", {"class" : "price"})[0].text
    price=extractIntFromText(Prix)
    Lesinfos.append(int(price))
    
    TelEssai = infos.select('div[class="AdviewContent"] > div[class="content"]')
    description = TelEssai[0].text.replace('\n','').strip()
    expression = r"0[0-9]([ .-/]?[0-9]{2}){4}"
    Telephone = re.search(expression,str(description))
    if Telephone:
        Telephone=Telephone.group()
    else: Telephone='NA'
    Lesinfos.append(Telephone)
    
    return Lesinfos

getinfos(url)
        




