import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
from getpass import getpass
from threading import Thread
import os

# Auth to git hub
def auth() :
    username = raw_input('Username:')
    password = getpass()
    return username,password

#Return soup from url
def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup



def getTop256Contributor(soup):
    contributors = soup.select("tr > td:nth-of-type(1) > a")
    Listcontributors = []
    for contributor in contributors:
        Listcontributors.append(contributor.text)
    # print contributors
    return Listcontributors

def getInformationFromContributor(Listcontributors, df):
    star_nb =0.0
    project_nb=0.0
    for contributor in Listcontributors:
        contributor_login = contributor
        user_url = "https://api.github.com/users/" + contributor_login + "/repos"
        projects_json = requests.get(url=user_url, auth=(username,password)).json()
        # print projects_json
        for project in projects_json:
            star_nb += project['stargazers_count']
            project_nb += 1
        score = star_nb/project_nb
        print 'Contributor : ' + contributor_login + '  :  ' + str(score)
        df = df.append(pd.Series({'contrib':contributor_login,'nb_star':score}, index=['contrib', 'nb_star']), ignore_index=True)
    return df


class DisplayThread(Thread):

    #Constructeur
    def __init__(self, Listcontributors, df, num_thread):
        Thread.__init__(self)
        self.Listcontributors = Listcontributors
        self.df = df
        self.num_thread = num_thread

    #On definit notre run
    def run(self):
        #On recupere le nb d artistes traites par thread
        contributors_by_thread = len(Listcontributors)/nb_thread
        #L indice du premier artiste traite
        first_contrib = self.num_thread * contributors_by_thread
        #L indice du dernier
        last_contrib = (self.num_thread + 1) * contributors_by_thread
        self.Listcontributors = self.Listcontributors[first_contrib:last_contrib]
        self.data_frame = getInformationFromContributor(self.Listcontributors, df)


threads = []
list_DF = []
nb_thread = os.sysconf("SC_NPROCESSORS_ONLN") * 2
df = pd.DataFrame(columns=['contrib', 'nb_star'])
# df_sorted = pd.DataFrame(columns=['contrib', 'nb_star'])
username, password = auth()
url = 'https://gist.github.com/paulmillr/2657075'
soup = getSoupFromUrl(url)
Listcontributors = getTop256Contributor(soup)


# On creer attends de threads que necessaire
for i in range(0,nb_thread):
    t = DisplayThread(Listcontributors, df, i)
    threads.append(t)
    t.start()

# On attends que tous les thread soient finis
for thread in threads:
    thread.join()
    list_DF.append(thread.data_frame)
    print list_DF


df_sorted = pd.concat(list_DF)

print "All threads finished"

print df_sorted.sort_values('nb_star')