__author__ = 'khalil'

import pdb
import urllib2
from bs4 import BeautifulSoup
page = urllib2.urlopen('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013').read()
soup = BeautifulSoup(page)
#print soup
#print soup.find_all('a')

#print soup.find_all('a')
#print soup.find_all("td", {"class": "montantpetit G"})
#for p in soup.find_all("td", {"class": "montantpetit G"}):
 #  print p.next
 #  print "euro %s" %
 #  print "habitant %s" %
 #  print "-----------" 

#soup.select("tr > td:nth-of-type(3)")
#print soup.select("tr > td:nth-of-type(3)")

#for p in soup.select("tr:nth-of-type(10) > td:nth-of-type(3)"):
   #print p.find_all("td",{ "class" : "montantpetit G" })
   #print " Euros par habitant  %s" % p.next
   #print
print soup.select("tr:nth-of-type(10) > td:nth-of-type(3)")[0].next
