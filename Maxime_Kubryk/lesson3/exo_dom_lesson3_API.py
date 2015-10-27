import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd


def crawling():

    page = requests.get('https://gist.github.com/paulmillr/2657075')
    soup = BeautifulSoup(page.text)

    f = open('login_list.csv', 'w')

    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        f.write(row.findAll('a')[0].contents[0] + "\n")

    f.close()

    return


def API():

    logins = pd.read_csv('login_list.csv', header=None)

    contributors = {log[0]: [] for log in logins.values}
    print(contributors)

    for login in logins.values:
        user = login[0]
        answer = requests.get("https://api.github.com/users/" + user + "/repos")

        answer = answer.json()

        print(user, len(answer))

        for i in range(len(answer)):
            repo_name = answer[i]['name']
            repo_stars = answer[i]['stargazers_count']

            print(repo_name, repo_stars)
            contributors[user] = contributors[user] + [repo_stars]

    print(contributors)
