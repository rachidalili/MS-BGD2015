# -- coding: utf-8 --
#!python3

#^^^^ Keep this line if you plan to use french characters (even in comments)
'''
Bonjour à tous,

En récap de notre cours de mardi je vous encourage à lire les parties de la doc Pandas 
que nous avons abordées : Groupby, Timeseries, Merge / Concat. 

Pour la semaine prochaine et notre dernier cours (amenez les mouchoirs) 
je vous propose un petit hackathon santé.

Peut-on établir un lien entre la densité de médecins par spécialité  
et par territoire et la pratique du dépassement d'honoraires ? 
Est-ce  dans les territoires où la densité est la plus forte que les médecins 
 pratiquent le moins les dépassement d'honoraires ? 
 Est ce que la densité de certains médecins / praticiens est corrélé 
 à la densité de population pour certaines classes d'ages (bebe/pediatre, 
    personnes agées / infirmiers etc...) ?

C'est un sujet assez ouvert pris du Hackathon "données de santé" de Etalab.
 Il y a un github qui contient une partie des données dont vous aurez besoin. 
 Vous pouvez compléter ça avec de l'INSEE et des données sur la démographie des médecins.

Amusez vous bien !
'''

'''
source de données: 
- https://github.com/SGMAP-AGD/DAMIR/tree/master/fichiers_supplementaires/rpps
Effectifs des médecins par spécialité, mode d'exercice et zone d'inscription
fichier R

--> il existe une API ! sur opendatasoft:
- http://public.opendatasoft.com/explore/dataset/depenses-dassurance-maladie-hors-prestations-hospitalieres/?tab=metas

https://github.com/SGMAP-AGD/DAMIR

'''
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
import re
from multiprocessing.dummy import Pool


#URL_LE_BONCOIN = "http://www.leboncoin.fr/voitures/offres/"
#region =  "aquitaine"
#REGIONS = ['aquitaine','ile_de_france','provence_alpes_cote_d_azur']
#voiture = "zoe"
#REGIONS = ['alsace','franche_comte','lorraine']
#voiture = "alpha 147"


def formURLlbc(region, modele):
    url= URL_LE_BONCOIN+region+'/?f=a&th=1&q='+modele
    return url

def crawlLeBonCoinUrlList(region, modele):
    '''
        Récupérer via crawling la liste des annonces pour la recherche 
        sur leboncoin.fr pour la région et le modele entres en parametre 
        Retourne une liste 
    '''
    #url = "http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&q=zoe" 
    url = formURLlbc(region, modele)
    print(url)
    r = requests.get(url)
    #print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_list = []
    listLbc= soup.findAll('div', class_='list-lbc')[0]
    #print(listLbc)
    for url in listLbc.select('a'):
        url_list.append(url.attrs['href'])
    return url_list

def crawlLeBonCoinAnnonce(url, dict_result):
    '''version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, 
    est ce que la voiture est vendue par un professionnel ou un particulier.
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = int(soup.findAll('span', class_='price')[0].attrs['content'])
    brand = soup.findAll('td', itemprop='brand')[0].text
    model = soup.findAll('td', itemprop='model')[0].text
    if model != "Zoe" : return
    year = int(re.sub('[\s+]', '', soup.findAll('td', itemprop='releaseDate')[0].text))
    selector = 'tr:nth-of-type(' + str(3) + ') td:nth-of-type(' + str(1) + ')'
    km = soup.findAll('div', class_="lbcParams criterias")[0]('table')[0].select(selector)[0].text
    km = re.sub('[\s+]', '', km)
    km = int(re.sub('KM', '', km))
    desc = soup.findAll('div', itemprop='description')[0].text
    rexp = re.compile(r'((?:0|\+33|0033)[ .]*[1-9][ .]*(?:[0-9][ .]*){8})')
    tel = rexp.search(desc)
    if tel :
        tel = tel.groups()[0]
        tel = re.sub('[\s+]', '', tel)
        tel = re.sub('[.]', '', tel) 
    rexp = re.compile(r'(Intens|Zen|Life)', re.IGNORECASE)
    version = rexp.search(desc)
    if version : version = version.groups()[0].lower()
    
    #img_tel = soup.findAll('img', class_="AdPhonenum")[0].attrs['src']
    pro = False
    if (soup.findAll('span', class_="ad_pro")):
       pro = True

    dict_result.update({ url : {
        "prix" : price,
        "marque" : brand,
        "modele" : model,
        "annee" : year,
        "kilometrage" : km,
        "tel" : tel,
    #    "url_img_tel" : img_tel,
        "pro" : pro,
        "version" : version
        }})


def retrieveQuoteAlpha(year):
    url = "http://www.lacentrale.fr/cote-voitures-alfa+romeo-147--+"+year+"-.html"
    r = requests.get(url)
    if (r.status_code != 200) : return None
    soup = BeautifulSoup(r.text, 'html.parser')
    cote = soup.findAll('span', class_="Result_Cote arial tx20")[0].text
    cote = re.sub('[\s+]', '', cote)
    cote = re.sub('[€]', '', cote)
    return int(cote)


def retrieveQuote(brand, model, version, year):
    if (version is None): return None
    url = "http://www.lacentrale.fr/cote-auto-"+brand.lower()+"-"+model.lower()+"-"+version.lower()+"+charge+rapide-"+str(year)+".html"
    r = requests.get(url)
    if (r.status_code != 200) : return None
    soup = BeautifulSoup(r.text, 'html.parser')
    cote = soup.findAll('span', class_="Result_Cote arial tx20")[0].text
    cote = re.sub('[\s+]', '', cote)
    cote = re.sub('[€]', '', cote)
    return int(cote)

## utilisation de tread pour paralléliser la récupération des moyennes

def retrieveData(url_list, NB_THREADS=50):

    #intialiazing result dict of type { user: meanStarGazers } 
    result_dict = {}
    # lock to serialize console output
    lock = threading.Lock()

    def do_work(dict_params):
        # updating dict with the Mean of StarGazersCount of all repos of user
        url = dict_params['url']
        crawlLeBonCoinAnnonce(url, dict_params['dict'])
        # pretend to do some lengthy work.
        # Make sure the whole print completes or threads can mix up output in one line.
        with lock:
            print(threading.current_thread().name,dict_params['url'])

    # The worker thread pulls an item from the queue and processes it
    def worker():
        while True:
            dict_params = q.get()
            do_work(dict_params)
            q.task_done()


    # Create the queue and thread pool.
    q = Queue()
    for i in range(min(NB_THREADS, len(url_list))):
     t = threading.Thread(target=worker)
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

    # stuff work items on the queue (in this case a dict with the user adn global dict to update).
    start = time.perf_counter()
    for url in url_list:
        dict_params = { 'url' : url, 'dict' : result_dict}
        q.put(dict_params)

    q.join()       # block until all tasks are done

    print('time:',time.perf_counter() - start)
    
    df = pd.DataFrame(result_dict, columns = result_dict.keys()).transpose()

    return df



### main ###

#user_df= crawlGitUrlList(URL_PAUL_MILLR)
#user_df = pd.read_csv('user.csv')
#df = retrieveAndSortStarGazersCountMeanList(user_df)
#print(df)
#url_list=[]
#for reg in REGIONS:
#    url_list.extend(crawlLeBonCoinUrlList(reg,voiture))
#df = retrieveData(url_list)
#pool = Pool(processes = 9)
#f = lambda x : retrieveQuote(x[0],x[1],x[2],x[3])

#df['argus'] = df[['marque','modele','version','annee']].apply(lambda x : retrieveQuote(x[0],x[1],x[2],x[3]), axis=1)
#df['superieur argus'] = df['argus'] < df['prix']
#df.to_csv('zoe_le_bon_coin.csv')

param= "page=1&affliste=0&affNumero=0&isAlphabet=0&inClauseSubst=0&nomSubstances=&typeRecherche=0&choixRecherche=medicament&txtCaracteres=Doliprane&btnMedic.x=10&btnMedic.y=17&btnMedic=Rechercher&radLibelle=2&txtCaracteresSub=&radLibelleSub=4"

params = { 'page':1, 'affliste':0, 'affNumero':0, 'isAlphabet':0, 'inClauseSubst':0, 
        'nomSubstances': '', 'typeRecherche':0, 'choixRecherche': 'medicament', 'txtCaracteres': 'Doliprane', 'radLibelle':2, 'txtCaracteresSub': '', 'radLibelleSub':4 }
url = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
r = requests.post(url, data=params)
print (r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)
balises  =soup.findAll(class_="standart")
names = [x.text for x in balises]
names = pd.Series(names)
names = names.str.strip()
print(names)

reg_string = r'(\d+,?\d*) (?:(\w|\s))+, ((?:\w|\s)+)'
regx = re.compile(reg_string)
print (names.str.findall(regx))

