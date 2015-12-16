# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:25:31 2015

@author: bibiane
"""

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
    rep=int(text.replace(u'\xa0', u'').replace(' ', ''))
    return rep 

""" Quand on veut obtenir l'année, on se rend compte qu'il faut juste modifier l'url apres
exercice= . On a pas besoin de mettre le year entre crochets car il combinera céjà
ce qui est entre le crochet url et le year"""

def getUrlFYear(year):
    year = str(year)
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
    return url

""" Quand on replace juste avec le premier replace,il reste un espace (1 048)
ce qui fait qu'il ne le reconnait pas en integer, d'où l'intéret du deuxième replace
pour rempacer cet espace """
    
url= 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013'

mairie2= getSoupfromurl(url)

Infos = mairie2.findAll("tr", {"td": ""})


"""Les informations que nous recherchons étant situées dans différents niveaux de <tr>, il faudrait que nous allions
chercher les numéros de <tr> concernés"""

"""  Ici les différentes positions des <tr> que nous cherchons """
""" 1ere étape: Les mettre """

Montants = [10, 14, 22, 27]

""" Les positions dans le td pour les informations recherchées à savoir l'Euros par habitant
et la moyenne de la strate sont situées entre 2 et 3e position respectivement dans
la balise <td> """

ChiffresRecherches = [2, 3]


InfosPrecises = mairie2.select('tr:nth-of-type(10) > td:nth-of-type(2)')
InfosPrecises

"""Il est important de préciser str() pour un entier """
""" ChiffresRecherches[0] Il prend le premier élément dans le tableau ChiffresRecherches """

def InfosofYear(year):
    url =  getUrlFYear(year)  
    mairie = getSoupfromurl(url)

    #""" J y ai passé des heures, en éffet dansl'élément Montants, il existe plusieurs chiffres, lui demander de 
    #faire : 'tr:nth-of-type('+ str(Montants) + ')' ne nous menera à rien, il nous affichera une erreur de type Unsupported or invalid CSS selector: 14,
    #car il y a plusieurs éléments dans la liste et il ne sait pas quoi faire """
    #""" D'où l'intéret obligatoire de la boucle """
    
    for Montant in Montants:
        print mairie.select('tr:nth-of-type('+ str(Montant) + ') > td:nth-of-type(4)')[0].text.replace(u"","")
        str_EuroHabitant = mairie.select('tr:nth-of-type('+ str(Montant) + ') > td:nth-of-type(' + str(ChiffresRecherches[0]) + ')')
        str_MoyenneStrate = mairie.select('tr:nth-of-type('+ str(Montant) + ') > td:nth-of-type(' + str(ChiffresRecherches[1]) + ')')
    
        EuroHabitant = extractIntFromText(str_EuroHabitant[0].text)
        print 'Euro par Habitant :', EuroHabitant
        MoyenneStrate = extractIntFromText(str_MoyenneStrate[0].text)
        print 'Moyenne par Strate :' , MoyenneStrate
        print '#######'

""" C'est une fonction qui retourne donc pas besoin du return en fin de fonction """

DebutYear=2010
FinYear=2014

for year in range(DebutYear,FinYear):
        print 'year', year
        InfosofYear(year)
        
        print 'Année suivante'
    
