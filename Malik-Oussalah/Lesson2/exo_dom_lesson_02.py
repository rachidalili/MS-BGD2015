import requests
from bs4 import BeautifulSoup

#########################################
#Creating functions for crawling process#
#########################################


#This function converts a text into an Integer
def getIntfromTxt(text):
    return int(text.replace(u'\xa0',u'').replace(' ',''))



#This function gets a html webpage and parses it
def GetSoupfromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text,'html.parser')

#This function prints information about "€ par habitant" and "Moyenne de la Strate" for a choosen year
def getInfoFromYear(year,url):
    listevoulu = [3,7,15,20]
    print "Année : " + str(year)
    print "############"
    for ope in listevoulu:
        start(ope,url,year)

#this function is used to get information about "€ par habitant" and "Moyenne de la Strate" for one Operation
def start(ope,url,year):
    soup = GetSoupfromUrl(url)
    lib = soup.findAll("tr",{"class":"bleu"})[ope]
    print lib.select('td:nth-of-type('+ str(4) + ')')[0].text
    print u"Euros par habitant : " + lib.select('td:nth-of-type('+ str(2) + ')')[0].text
    print u"Moyenne de la Strate : " + lib.select('td:nth-of-type('+ str(3) + ')')[0].text
    print " "
    
    
##################################################
#Bonus function : choosing the year through input#
##################################################


def Usermode():
    y = input("Entrer l'année : ")
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(y)
    getInfoFromYear(y,url)


#############################################################
#Configuration : Getting informations from Year 2010 to 2014#
#############################################################

Years =range(2010,2014)
for y in Years:
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(y)
    getInfoFromYear(y,url)