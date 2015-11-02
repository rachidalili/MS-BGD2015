import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from collections import OrderedDict


def crawling():

    page = requests.get('https://gist.github.com/paulmillr/2657075')
    soup = BeautifulSoup(page.text)

    f = open('login_list.csv', 'w')

    for row in soup.findAll('table')[0].tbody.findAll('tr > td'):
        f.write(row.findAll('a')[0].contents[0] + "\n")

    f.close()

    return


def API():

    logins = pd.read_csv('login_list.csv', header=None)

    contributors = {log[0]: {'mean_stars': 0, 'count': 0} for log in logins.values}
    print(contributors)

    for login in logins.values:
        user = login[0]
        answer = requests.get("https://api.github.com/users/" + user +
                              "/repos", auth=('maxkub', '****'))

        answer = answer.json()

        print(user, len(answer))

        for i in range(len(answer)):
            repo_name = answer[i]['name']
            repo_stars = answer[i]['stargazers_count']

            #print(repo_name, repo_stars)
            contributors[user]['mean_stars'] = contributors[user]['mean_stars'] + repo_stars
            contributors[user]['count'] = contributors[user]['count'] + 1

    for key, val in contributors.items():
        mean = contributors[key]['mean_stars']
        count = float(contributors[key]['count'])
        contributors[key] = mean / count

    d_descending = OrderedDict(sorted(contributors.items(),
                                      key=lambda kv: kv[1], reverse=True))

    print()

    for key, val in d_descending.items():
        print('%20a  %7.3f' % (key, val))

    # for key in keys:
    #    print('%20a  %7.3f' % (key, contributors[key]))
