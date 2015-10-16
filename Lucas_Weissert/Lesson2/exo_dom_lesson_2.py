import requests
import pprint
from bs4 import BeautifulSoup
from threading import Thread
import time
import os
from bs4 import BeautifulSoup


def extractIntFromText(text):
  return int(text.replace(u'\xa0', u'').replace(' ' ,''))

def getUrl(year):
    year = str(year)
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
    return url

def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def GetReportFromYear(year):
    url =  getUrl(year)  
    soup = getSoupFromUrl(url)
    rapport = {}
    result = {}
    
    #Pour chacun des libelles on recupere les deux informations qui nous interesse
    for libelle in libelles:
        #Information sous forme de str
        str_EuroParHabitant = soup.select('tr:nth-of-type('+ str(libelle) + ') > td:nth-of-type(' + str(information_by_libelle[0]) + ')')
        str_MoyenneStrate = soup.select('tr:nth-of-type('+ str(libelle) + ') > td:nth-of-type(' + str(information_by_libelle[1]) + ')')
        #Information parse en int
        EuroParHabitant = extractIntFromText(str_EuroParHabitant[0].text)
        MoyenneStrate = extractIntFromText(str_MoyenneStrate[0].text)

    result["EuroParHabitant"] = EuroParHabitant
    result["MoyenneStrate"] = MoyenneStrate
    rapport[year] = result

    return rapport

#Creation de notre class qui va afficher les informations du thread
class DisplayThread(Thread):

    #Constructeur
    def __init__(self, year):
        Thread.__init__(self)
        self.year = year

    #On definit notre run
    def run(self):
        rapports[self.year] = GetReportFromYear(self.year)

#Map des rapport
rapports = {}
#On recupere le nombre de thread maximum
nb_thread = os.sysconf("SC_NPROCESSORS_ONLN") * 2
#Tableau de threads
threads = []
#Tableau des annees
years = ['2010', '2011', '2012', '2013']
#On regarde les positions des informations qui nous interessent (position des tr)
libelles = [10, 14, 22, 27]
#On regarde la postion des information euros et moyenne dans les td
information_by_libelle = [2, 3]
# On creer attends de threads que necessaire
for i in range(0,len(years)):
    t = DisplayThread(years[i])
    threads.append(t)
    t.start()
# On attends que tous les thread soient finis
for thread in threads:
    thread.join()

print "All threads finished"
#On affiche tous les rapport
for p in rapports:
    print "Rapport " + p + " : " + str(rapports[p])


