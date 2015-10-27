# -- coding: utf-8 --
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
from urllib.parse import urlparse
from urllib.parse import urljoin


url = "https://gist.github.com/paulmillr/2657075"
github_token= "6ccaca814c800646fdb0714caaf656552839569b"

def crawlGitUrlList(url):
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

#user_df= crawlGitUrlList(url)
#print(user_df)

repos = 'https://github.com/spicyj/react'
gitbub_auth_url= 'https://api.github.com/authorizations/'
params= { 'Authorization': 'TOK:'+github_token+'' }

r = requests.get( 'https://api.github.com/authorizations/',
                auth=('AurelienGalicher',github_token))
print(r)
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    print ("spicyj repository created: %s" % repoItem['created_at'])



GITHUB_API = 'https://api.github.com'



def authentification():
    #
    # User Input
    #
    username = input('Github username: ')
    password = input('Github password: ')
    #
    # Compose Request
    #
    

    url = urljoin(GITHUB_API, 'authorizations')
    print(url)
    payload = {}
    res = requests.post(
        url,
        auth = (username, password),
        data = json.dumps(payload),
        )
    print(res.text)


