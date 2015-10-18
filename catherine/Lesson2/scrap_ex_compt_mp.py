# -*- coding: utf-8 -*-
# __author__ = 'catherine'


# Exercice de scraping
# Objectif : récupérer des données sur les exercices comptables de la mairie
#            de Paris entre 2009 et 2013
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
# Récupérer le parsing Soup de la page de la mairie de Paris correspondant
# à l'exercice d'une année donnée
#
def getSoup4Exercice(annee):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+str(annee)
    return getSoupFromUrl(url)

#
# Pour la recherche des tags qui nous intéressent, on filtrera en selectionnant les lignes
# de tableaux dont la classe est 'bleu', qui ont une cellule ayant pour classe 'montantpetit'
# et dont le contenu de la cellule 'montantpetit' commence par 'en %'
#


def has_montantpetit_en_pct(tag):
    result = False
    if tag.has_attr('class') and ('bleu' in tag.attrs['class']):
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
    return result


#
# Convertir le montant de la cellule correspondante dans le flow HTML en valeur entière
#
def textAmount2int(text):
    result = text[0].contents[0].replace(' ', '').replace('&nbsp;', '')
    return int(result)

#
# Renvoyer sous la forme d'un dictionnaire à 4 entrées (A,B,C et D)
# les montants recherchés pour l'exercice correspondant à l'année
# passée en paramètre
#


def getAmounts4Exercice(annee):
    result = {}
    try:
        soup = getSoup4Exercice(annee)
        tb_lines = soup.find_all(has_montantpetit_en_pct)
        i = 0
        attributes = ["A", "B", "C", "D"]
        for line in tb_lines:
            if attributes[i] not in result.keys():
                result[attributes[i]] = {}
            result[attributes[i]]['Euros par habitant'] = {}
            result[attributes[i]]['Moyenne de la strate'] = {}
            result[attributes[i]]['Euros par habitant'] = textAmount2int(line.select('td:nth-of-type(1)'))
            result[attributes[i]]['Moyenne de la strate'] = textAmount2int(line.select('td:nth-of-type(2)'))
            i += 1
    except:
        pass
    return result


def print_exercice(annee):
    print("===============")
    print("Exercice "+str(annee))
    print("===============")
    exercice = getAmounts4Exercice(annee)
    attributes = ["A", "B", "C", "D"]
    if len(exercice) == 0:
        print("Pas de résultat pour "+str(annee))
    else:
        for att in attributes:
            print(att+" = {"+str(exercice[att]['Euros par habitant'])+","+str(exercice[att]['Moyenne de la strate'])+"}")


# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testExerciceComptable(self):
        for i in range(2009, 2013):
            print_exercice(i)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
