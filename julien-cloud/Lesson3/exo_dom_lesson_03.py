import urllib2
import re
from bs4 import BeautifulSoup
import json

URL_INDEX = "https://gist.github.com/paulmillr/2657075"
GITHUB_ACCESS_TOKEN = open('github_access_token', 'r').read()

users = []

# Read users from GitHub most active page
html = urllib2.urlopen(URL_INDEX).read()
soup = BeautifulSoup(html, 'html.parser')
nodes = soup.find('article').find('table').findAll('tr')
for node in nodes:
    if node.find('th').get_text() != "#":  # parse out the header row
        login = node.find('td').find('a').get_text().encode('utf-8').strip()
        if (len(login) > 0):
            users.append({'login': login})

# For each user, fetch the list of repos
for i in range(0, len(users)):
    query = "https://api.github.com/users/%s/repos?access_token=%s" % (users[i]['login'], GITHUB_ACCESS_TOKEN)
    response = urllib2.urlopen(query).read()
    repos = json.loads(response)
    stargazers_sum = 0.
    for repo in repos:
        stargazers_sum += repo['stargazers_count']
    users[i]['stargazers_avg'] = stargazers_sum / len(repos)
    print "%s/%s" % (i + 1, len(users))

# Sort the users table
sorted_users = sorted(users, key=lambda user: user['stargazers_avg'])

# Print out
for user in users:
    print "%s: %0.2f" % (user['login'], user['stargazers_avg'])
