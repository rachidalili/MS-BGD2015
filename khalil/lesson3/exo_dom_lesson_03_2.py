mport urllib2
from bs4 import BeautifulSoup
import re
from github3 import login
import operator
import urllib2
import json


url = "https://gist.github.com/paulmillr/2657075"
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

gh = login('chkhalil', password='bismallahazerty123A')
dict_rank = {}

def user_note(user_name):
    cumulated_stars = 0
  
    new_user = gh.user(user_name)   #'Ocramius'
   
    json_repos = new_user.repos_url   #check why some repo are not returned
    response = urllib2.urlopen(json_repos)
    data = json.load(response) 
    
    for i in range(0,len(data),1):    
        cumulated_stars += data[i]["stargazers_count"]
    note = cumulated_stars / float(len(data))
   
    return (note,new_user.name)

for i in range(1,257,1):
   complete_name = soup.select("table > tbody > tr:nth-of-type("+str(i)+")")[0].find('td').get_text()
   pseudo = soup.select("table > tbody > tr:nth-of-type("+str(i)+")")[0].find('a').get_text()
   note,name = user_note(pseudo)
   dict_rank[name]= note


sorted_dict_rank = reversed(sorted(dict_rank.items(), key=operator.itemgetter(1)))
result = list(sorted_dict_rank)
count = 1
for i in result: 
   print "user %s has average note equal to %s and has rank %s" %(i[0],i[1],count)
   count += 1
