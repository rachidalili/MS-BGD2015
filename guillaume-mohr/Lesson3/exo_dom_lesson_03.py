# coding: utf8

# Script tested with Python 3.5.0 and 2.7.10
# Course INFMDI 721 - Lesson 3
# Author : Guillaume MOHR

# IMPORTANT   : the script nees an authentification to GitHub
#               In order to execute it, a valide username / password
#               or username / token have to be submitted at the prompt

# To improve compatibility with Python 2.x:
from __future__ import unicode_literals 

import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from numpy import mean
from getpass import getpass
import pandas as pd
from sys import version_info


def authentification():
    """
    Since this script requires more than 60 API request / hours,
    we need to authentificate as a GitHub user.
    Returns:
    --------
    tuple (username, password)
    """
    # To get user input, we need to test Python version :(
    if version_info[0] > 2:
        username = input('GitHub username:')
    else:
        username = raw_input('GitHub username:')
    password = getpass()
    r = requests.get('https://api.github.com/user', auth=(username, password))
    if r.status_code != 200:
        print('Incorrect username/password, please retry')
        return authentification()
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
    users = [tr.select_one('a').text for tr in soup('tbody')[0].select('tr')]
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
    # We get a basic authentification method
    auth = authentification()
    # We get the list of user by scrapping
    users = getContributors(auth)
    # Using GitHub API we launch several threads to request repositories info
    pool = Pool(processes=max_workers)
    gUAS = lambda u : getUserAverageStars(u, auth) # partial function used in map
    user_star = [(user, score) for user, score in zip(users, pool.map(gUAS, users))]
    # Sort and put in a pandas dataframe
    user_star.sort(key=lambda x: x[1], reverse=True)
    dat = pd.DataFrame(data=list(zip(*user_star)), index=['Contributor', 'StarScore']).T
    return dat


if __name__ == '__main__':
    # Main function
    rank = rankContributors()
    # Write the results to a file
    rank.to_csv('mostStarredContributors')
    # Print the result to the screen
    print(rank)