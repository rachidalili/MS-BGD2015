# Script tested with Python 3.4
# Course INFMDI 721 - Lesson 3
# Author : Guillaume MOHR

# IMPORTANT 1 : the script is written for Python 3.4
#               it uses the standard library concurrent.futures
#               which in this case increases dramatically the speed
#               of the program with only a few more lines of code. 

# IMPORTANT 2 : the script nees an authentification to GitHub
#               In order to execute it, a valide username / password
#               or username / token have to be submitted at the prompt


import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from numpy import mean
from getpass import getpass
import pandas as pd


def authentification():
    """
    Since this script requires more than 60 API request / hours,
    we need to authentificate as a GitHub user.
    Returns:
    --------
    tuple (username, password)
    """
    username = input('GitHub username:')
    password = getpass()
    r = requests.get('https://api.github.com/user', auth=(username, password))
    if r.status_code != 200:
        print('Incorrect username/password, please retry')
        (username, password) = authentification()
    return (username, password)


def getContributors(auth):
    """
    Get a list of the most active GitHub users, via crawling
    Returns:
    --------
    A list of usernames
    """
    users = []
    r = requests.get(url='https://gist.github.com/paulmillr/2657075/',
            auth=auth)
    soup = BeautifulSoup(r.text, 'html.parser')
    trs = soup('tbody')[0].select('tr')
    for tr in trs:
        users.append(tr.select_one('a').text)
    return users


def getUserAverageStars(user, auth):
    """
    Using GitHub API, get the average star counts for each repository owned
    by a user.
    Parameters:
    -----------
    user - a valid GitHub username
    Returns:
    --------
    average number of stars
    """
    url = 'https://api.github.com/users/{}/repos'.format(user)
    r = requests.get(url=url, auth=auth)
    stars = [rep['stargazers_count'] for rep in r.json()]
    return mean(stars)


def rankContributors(max_workers=50):
    """
    Rank the 256 most active GitHub users by the number of stars
    of the repositories they own.
    We send the requests asynchronously otherwise it takes too much
    time (256 requests).
    Returns:
    --------
    A Pandas DataFrame with a column of users' name and their average score
    """
    auth = authentification()
    user_star = [] # result dictionary 
    users = getContributors(auth) # list of users
    gUAS = lambda u : getUserAverageStars(u, auth) # partial function used in map
    # Launch the concurrent threads 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        user_star = [(user, score) for user, score in zip(users, executor.map(gUAS, users))]
    # Sort and put in a pandas dataframe
    user_star.sort(key=lambda x: x[1], reverse=True)
    dat = pd.DataFrame(data=list(zip(*user_star)), index=['Contributor', 'StarScore']).T
    return dat


if __name__ == '__main__':
    rank = rankContributors()
    rank.to_csv('mostStarredContributors')
    print(rank)
