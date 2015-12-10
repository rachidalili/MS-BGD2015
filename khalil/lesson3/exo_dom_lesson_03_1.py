import urllib2
from bs4 import BeautifulSoup
import re


url = "https://gist.github.com/paulmillr/2657075"

html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
for i in range(1,257,1):
   print "le rang de l'utilisateur %s est %s"  %(soup.select("table > tbody > tr:nth-of-type("+str(i)+")")[0].find('td').get_text(),str(i))
