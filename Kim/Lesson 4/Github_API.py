# coding: utf8

import requests
from bs4 import BeautifulSoup
from github import Github
import github3
import json
import time


def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

TOKEN = 'c98a152e95e69a81b351ecc63514a228d6f6eb16'


url = 'https://gist.github.com/paulmillr/2657075'
soup = getSoupFromUrl(url)
Contributors = soup.findAll("article", { "class" : "markdown-body entry-content" })[0]
#tables = Contributors.findAll("table",{"cellspacing":"0"})[0]
tbodys = Contributors.findAll("tbody")[0]
trs = tbodys.findAll("tr")
liste_href = []
for tr in trs:
    tds =  tr.select('td:nth-of-type(1) ')[0]
    #href_tags = tds.findAll(href=True)
    href_tags = tds.findAll("a")
    for href_tag in href_tags:
       #print href_tag['href']
       #liste_href.append(href_tag['href'])
        #print href_tag.text
        liste_href.append(href_tag.text)
        
#Liste_href contient les noms des 256 plus gros contributeurs de github
#print liste_href


#create github instance using an authentification token
g = Github(TOKEN)
all_contrib_dict = {}

for url_git in liste_href :  
    m = 0
    total_stargarzers_nbr = 0
    for repo in g.get_user(url_git).get_repos():
        m = m +1
        #print"nom du  repertoire: ", repo.name
        if (repo.name != "code-problems"): #ce repo pose pb, le chunter
            pg_list = list( repo.get_stargazers())
            #print len(pg_list) #renvoie le nombre de stargazers sur ce repo
            total_stargarzers_nbr = total_stargarzers_nbr + len(pg_list)
        time.sleep(2)
    moy_user = total_stargarzers_nbr/m
    print "\n" + url_git + " a une moyenne de " + str(moy_user)
    all_contrib_dict[url_git] = moy_user
    time.sleep(5)
        
for w in sorted(all_contrib_dict, key=all_contrib_dict.get, reverse=True):
  print w, all_contrib_dict[w]


       