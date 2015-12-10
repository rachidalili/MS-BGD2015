# coding: utf8

import requests
from bs4 import BeautifulSoup
import operator
import pandas as pd

headers = {'Authorization': 'token afee50e68d303520fc2a37fb1b1fe3552247bf64'}
def getSoupFromUrl(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def storeMeanStargazers(reposList):
     topUsers ={}
     for user in reposList:
        req = requests.get('https://api.github.com/users/'+user+'/repos',headers=headers)
        stargazers_tot=0;
        for repos in req.json():
            stargazers_tot += repos['stargazers_count']
        topUsers[user]= stargazers_tot/len(req.json())
     return topUsers

def showTopUsers(topUsers):
    df = pd.DataFrame(sorted(topUsers.items(), key=operator.itemgetter(1),reverse=True))
    df.columns=['user','score']
    df.to_csv("gitTopUsers.csv")


def getGitHubTop(topCount):
    url = 'https://gist.github.com/paulmillr/2657075';
    soup = getSoupFromUrl(url)
    div = soup.findAll("div", { "id" : "readme" })[0]
    table = div.findNext("table")
    reposList=[]
    for tr in table.findAll("tr"):
        th = tr.findNext("th")
        topNumber=th.text.replace('#','')
        if len(topNumber) :
            if int(topNumber)>topCount :
                break
            reposList.append(tr.findNext("a").text)
    topUsers=storeMeanStargazers(reposList)
    showTopUsers(topUsers)

getGitHubTop(256)





