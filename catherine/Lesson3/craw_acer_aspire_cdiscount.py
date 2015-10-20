__author__ = 'catherine'

#
# Exercice cours : récupérer nom des produits, images, ancien et nouveau prix
# sur une page cdiscount
# on travaille sur : http://www.cdiscount.com/ct-ordinateurs-portables/acer+aspire.html#_his_
#


#
# On utilise les bibliothèques python suivantes :
#   - requests ==> pour faire des requêtes HTTP et récupérer les pages HTML qui nous intéressent
#   - beautifulSoup ==> pour parser le HTML et y récupérer des éléments précis
#
import requests
from bs4 import BeautifulSoup
import unittest


#
# Récupérer le parsing Soup d'une page HTML accessible via le paramètre url
#
def getSoupFromUrl(url):
    #Execute q request toward Youtube
    request = requests.get(url)
    #parse the restult of the request
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup


#
# Fonction de filtrage de la soupe
# On prend les tags div de class prDtBloc
#
def is_cdiscount_prod_bloc(tag):
    result = False
    if tag.has_attr('class') and ('prDtBloc' in tag.attrs['class']):
        result = True
    return result
"""
        tag_contents = tag.find_all()
        for child in tag_contents:
            if (child.name == 'td' and
                child.has_attr('class') and
                'montantpetit' in child.attrs['class']):
                child_contents = child.contents
                for c in child_contents:
                    if (str(c).startswith('en %') and not str(c).endswith('fonct.')):
                        result = True
                        break
                if (result == True):
                    break
"""

soup = getSoupFromUrl("http://www.cdiscount.com/ct-ordinateurs-portables/acer+aspire.html#_his_")
selection = soup.find_all('div')
print(selection[0])
#.find_all(is_cdiscount_prod_bloc)