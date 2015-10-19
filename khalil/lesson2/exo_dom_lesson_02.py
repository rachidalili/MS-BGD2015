__author__ = 'khalil'

import pdb
import urllib2
from bs4 import BeautifulSoup


def scrap(year):
   page = urllib2.urlopen('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013').read()
   soup = BeautifulSoup(page)
   #print soup.find_all("td", {"class": "montantpetit G"}) 
   print "A Euro par habitant %s dans l'annee %s" %(soup.find_all("td", {"class": "montantpetit G"})[1].next, year)
   print "A Euro par strate %s  dans l'annee %s" %(soup.find_all("td", {"class": "montantpetit G"})[2].next, year)
   print "B Euro par habitant %s  dans l'annee %s " %(soup.find_all("td", {"class": "montantpetit G"})[4].next, year)
   print "B Euro par strate %s   dans l'annee %s" %(soup.find_all("td", {"class": "montantpetit G"})[5].next, year)
   print "C Euro par habitant %s  dans l'annee %s " %(soup.find_all("td", {"class": "montantpetit G"})[10].next, year)
   print "C Euro par strate %s   dans l'annee %s" %(soup.find_all("td", {"class": "montantpetit G"})[11].next, year)
   print "D Euro par habitant %s  dans l'annee %s " %(soup.find_all("td", {"class": "montantpetit G"})[13].next,year)
   print "D Euro par strate %s   dans l'annee %s" %(soup.find_all("td", {"class": "montantpetit G"})[14].next,year)

def main():
   scrap(2010)
   scrap(2011)
   scrap(2012)
   scrap(2013)

if __name__ == '__main__':
  main()
