# -- coding: utf-8 --
#!python3

#^^^^ Keep this line if you plan to use french characters (even in comments)
#CBonsoir à tous,

#En conclusion du cours de ce matin voici des ressources pour approfondir les concepts abordés:
#- API http://readwrite.com/2013/09/19/api-defined, http://www.quora.com/In-laymans-terms-what-is-an-API-1
#- Verbes HTTP: http://micheltriana.com/2013/09/30/http-verbs-in-a-rest-web-api/
#- JSON http://stackoverflow.com/questions/383692/what-is-json-and-why-would-i-use-it﻿
#- OAuth https://developers.google.com/identity/protocols/OAuth2
#- Un must see pour montrer les potentialités de Pandas https://vimeo.com/59324550

#L'exercice pour le cours prochain est le suivant: 
#- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
#- En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories qui leur appartiennent. Pour finir classer ces 256 contributors par leur note moyenne.﻿

# list of most activre user https://gist.github.com/paulmillr/2657075
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import  base64
import operator
import sys
from requests.auth import HTTPBasicAuth
import numpy as np
import threading
from queue import Queue
import time


URL_PAUL_MILLR = "https://gist.github.com/paulmillr/2657075"
github_token = "6ccaca814c800646fdb0714caaf656552839569b"
git_login = "AurelienGalicher"
GITHUB_API = 'https://api.github.com'

def crawlGitUrlList(url):
    '''
        Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
        Retourne une dataframe avec nom et url
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    index_list = []
    url_list = []
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        classement = int(row.findAll('th')[0].contents[0].replace('#',''))
        url_column = row.findAll('td')[0].select('a')[0].attrs['href']
        url_list.append(url_column)
        index_list.append(classement)
    user_df= pd.DataFrame(url_list,index=index_list)
    user_df.columns=['url']
    user_df['user']=user_df['url'].str.replace('https://github.com/','')
    return user_df



def retrieveStarGazersCountMean(user):
    '''
    En utilisant l'API github https://developer.github.com/v3/ 
    récupére pour 'user' le nombre moyens de stars des repositories
    '''
    user_repos_url = GITHUB_API+'/users/'+user+'/repos'
    r= requests.get(user_repos_url, auth=HTTPBasicAuth(git_login, github_token))
    repos_json_list = json.loads(r.text)
    list_stargazers_count=[]
    for repo in repos_json_list :
        if repo["stargazers_count"]:
           list_stargazers_count.append(repo["stargazers_count"])
    mean_repos_list = sum(list_stargazers_count)/ float(len(list_stargazers_count))
    return mean_repos_list


## utilisation de tread pour paralléliser la récupération des moyennes

def retrieveAndSortStarGazersCountMeanList(user_df, NB_THREADS=50):

    #intialiazing result dict of type { user: meanStarGazers } 
    result_dict = {}
    # lock to serialize console output
    lock = threading.Lock()

    def do_work(dict_params):
        # updating dict with the Mean of StarGazersCount of all repos of user
        user= dict_params['user']
        dict_params['dict'].update({user: retrieveStarGazersCountMean(user)})
        # pretend to do some lengthy work.
        # Make sure the whole print completes or threads can mix up output in one line.
        with lock:
            print(threading.current_thread().name,dict_params['user'])

    # The worker thread pulls an item from the queue and processes it
    def worker():
        while True:
            dict_params = q.get()
            do_work(dict_params)
            q.task_done()


    # Create the queue and thread pool.
    q = Queue()
    for i in range(min(NB_THREADS, len(user_df.index))):
     t = threading.Thread(target=worker)
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

    # stuff work items on the queue (in this case a dict with the user adn global dict to update).
    start = time.perf_counter()
    for user in user_df['user']:
        dict_params = { 'user' : user, 'dict' : result_dict}
        q.put(dict_params)

    q.join()       # block until all tasks are done

    print('time:',time.perf_counter() - start)
    df = pd.Series(result_dict, name='average StarGazers TOP 256 popular git users')
    df.index.name = 'user'
    df.columns=['average StarGazers']
    df.reset_index()
    return df.sort_values(ascending=0)



### main ###

user_df= crawlGitUrlList(URL_PAUL_MILLR)
#user_df = pd.read_csv('user.csv')
df = retrieveAndSortStarGazersCountMeanList(user_df)
print(df)
