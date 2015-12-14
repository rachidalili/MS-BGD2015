
__author__ = 'omakil'


from bs4 import BeautifulSoup
import json
import requests

#urls
api_url = "https://api.github.com"
url= "https://github.com"
urlpaul="https://gist.github.com/paulmillr/2657075"

# fonctions

def getSoupFromUrl(url):
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    return s

def getTagsFromSoup(soup):
    tags = soup.find_all(lambda tag: tag.name == 'a' \
                        and tag.parent.name == 'td' \
                        and tag.attrs['href'].find(url) != -1)
    return tags

def connectToken(header):
    r= requests.get(api_url+"/user", headers=header)
    return r.status_code


def getUserReposFromTag(user, header):
    username = user.contents[0]
    r = requests.get(api_url+"/users/"+username+"/repos?type=owner", headers=header)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return None

def getUserReposStars(user, header):
    repos = getUserReposFromTag(user, header)
    stars = 0
    if repos is not None:
        for repo in repos:
            stars += repo['stargazers_count']
            mean= stars/len(repos)
        return mean
    else:
        return stars



# traitements

my_token = 'a41aa3b32a48986091d9522bc368740bc90ffd3e' #token a supprimer 
header = {"Authorization": "token "+my_token}
soup = getSoupFromUrl(urlpaul)
tags = getTagsFromSoup(soup)
df = ["username","stars"]
status = connectToken(header)

if  status == 200:
    i = 1
    for tag in tags:
        percent= (100*i)/256.0
        print(str(percent)+"%"+" terminee")
        mean = getUserReposStars(tag, header)
        df.append([tag.contents[0], mean])
        i += 1
        df = sorted(df, key=lambda contributor: contributor[1], reverse=True)
    for entry in df:
        print(entry[0] + " a "+str(entry[1])+ " etoiles ")
else:
    print("Unauthorized")

