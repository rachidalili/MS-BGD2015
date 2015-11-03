# coding: utf8
#from __future__ import unicode_literals
#L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
#Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire,
#est ce que la voiture est vendue par un professionnel ou un particulier.
#Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

#Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
#Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿

#On fige sur une région
#>Page de recherche pro et particulier > http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=renault+zo%E9
#> On vérifie la version dans le titre (zen, life ou intens) pour éliminer les mauvais résultats (OK)
#>On détermine si c'est pro ou pas (présence de (pro) ou pas) (OK)
#>On peut déjà extraire le prix (OK)
#>On extrait également les liens (OK)
#>>On parcourt les liens et on extrait:
#>> l'année (Année-modèle : 2014 ) (OK)
#>> Kilométrage (OK)
#>> Téléphone du proprio (OK)
#import pandas as pd
import json
import re
import requests
from bs4 import BeautifulSoup
#from pytesser import *


def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def getPrixAndPro(renault):
    prix = float(renault.find("div",{"class","price"}).text.encode('utf-8').replace(" ","").replace("\xc2\xa0\xe2\x82\xac","").replace("\n",""))
    pro = ( re.compile("\(.+\)").search(renault.find("div",{"class","category"}).text) is not None)
    #autre version: pro = b.find("div",{"class","category"}).text.encode('utf-8').replace(" ","").replace("\xc2\xa0\xe2\x82\xac","").replace("\n",""))
    return prix,pro

def getPhoneNumber(renaultInSoup):
    phoneNumberAvailable = re.compile("(\d{2})\D{0,2}(\d{2})\D{0,2}(\d{2})\D{0,2}(\d{2})\D{0,2}(\d{2})").search(renaultInSoup.findAll('div',{'class','content'})[0].text)
    phoneNumber = phoneNumberAvailable.group() if phoneNumberAvailable is not None else None
    return phoneNumber

def getKilometrageAndAnnee(renaultInSoup):
    kilometrage = str([(tata.td.text[:-2].replace(' ','')) for tata in renaultInSoup.findAll('tr') if (tata.th is not None and tata.th.text == u'Kilométrage :')])[1:-1]
    annee = re.sub(r'[ \n]', '', renaultInSoup.find('td', {'itemprop':'releaseDate'}).text)
    # A enquêter pour comprendre pourquoi annee n'est pas détectée annoyingly weird
    #[(tata.td.text) for tata in renaultInSoup.findAll('tr') if (tata.th is not None and tata.th.text in [u'Kilométrage :',u'Année-modèle :'])]
    return kilometrage, annee

def getVoitures(url):

  soup = getSoupFromUrl(url)

  listeOffresVoitures = soup.findAll("div",{"class","detail"})

  renaultBonnesVersions = soup.findAll(title=re.compile("Life|Intens|Zen",re.IGNORECASE))

  renaultTrouvees = list()
  for renault in renaultBonnesVersions:
      url                = renault['href']
      prix, pro          = getPrixAndPro(renault)
      renaultInSoup      = getSoupFromUrl(url)
      phoneNumber        = getPhoneNumber(renaultInSoup)
      kilometrage, annee = getKilometrageAndAnnee(renaultInSoup)
      renaultTrouvees.append((url, prix, pro, phoneNumber, kilometrage, annee))
  return renaultTrouvees

urlsAParcourir = [
    "http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=renault+zo%E9",
    "http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?f=a&th=1&q=renault+zo%C3%A9",
    "http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&q=renault+zo%C3%A9"]

renaultTrouveesPartout = list()
[renaultTrouveesPartout.extend(getVoitures(url)) for url in urlsAParcourir]

df = pandas.DataFrame(data, columns=['Url', 'Prix', 'Pro', 'Téléphone', 'Kilométrage','Année'])
