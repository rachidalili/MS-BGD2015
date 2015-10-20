__author__ = 'Siham Laaroussi'

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

for i in range(2010, 2015):
    
    soup=getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(i))
    Titre = soup.select("tr:nth-of-type(3) > td:nth-of-type(2)")
    annee = soup.select("tr:nth-of-type(3) > td:nth-of-type(3)")
    print str(Titre[0].next) + " CORRESPONDANT A L'ANNEE "+ str(annee[0].next)
    print ("\n")
    Euros_par_habitant = soup.select("tr:nth-of-type(10) > td:nth-of-type(2)")
    Moyenne_de_la_strate = soup.select("tr:nth-of-type(10) > td:nth-of-type(3)")
    print "TOTAL DES PRODUITS DE FONCTIONNEMENT = A, Euros par Habitant "+ Euros_par_habitant[0].next
    print "TOTAL DES PRODUITS DE FONCTIONNEMENT = A, Moyenne de la strate "+ Moyenne_de_la_strate[0].next

    Euros_par_habitant = soup.select("tr:nth-of-type(14) > td:nth-of-type(2)")
    Moyenne_de_la_strate = soup.select("tr:nth-of-type(10) > td:nth-of-type(3)")
    print "TOTAL DES CHARGES DE FONCTIONNEMENT = B, Euros par Habitant "+ Euros_par_habitant[0].next
    print "TOTAL DES CHARGES DE FONCTIONNEMENT = B, Euros par Habitant "+ Moyenne_de_la_strate[0].next
    
    Euros_par_habitant = soup.select("tr:nth-of-type(22) > td:nth-of-type(2)")
    Moyenne_de_la_strate = soup.select("tr:nth-of-type(10) > td:nth-of-type(3)")
    print "TOTAL DES RESSOURCES D'INVESTISSEMENT = C, Euros par Habitant "+ Euros_par_habitant[0].next
    print "TOTAL DES RESSOURCES D'INVESTISSEMENT = C, Euros par Habitant "+ Moyenne_de_la_strate[0].next
    
    Euros_par_habitant = soup.select("tr:nth-of-type(27) > td:nth-of-type(2)")
    Moyenne_de_la_strate = soup.select("tr:nth-of-type(10) > td:nth-of-type(3)")
    print "TOTAL DES EMPLOIS D'INVESTISSEMENT = D, Euros par Habitant "+ Euros_par_habitant[0].next
    print "TOTAL DES EMPLOIS D'INVESTISSEMENT = D, Euros par Habitant "+ Moyenne_de_la_strate[0].next
    
    print ("============================")
