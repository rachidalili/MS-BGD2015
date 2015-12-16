# coding: utf8
# Sujet: Peut-on établir un lien entre la [ (densité de médecins) par (spécialité)  et par (territoire)] et la [pratique du (dépassement d'honoraires)] ?
#> http://www.data.drees.sante.gouv.fr/TableViewer/tableView.aspx

# Est-ce  dans les [(territoires) où la (densité est la plus forte)] que les médecins  pratiquent [(le moins les dépassement d'honoraires)] ?
# Est ce que la [(densité) de (certains médecins / praticiens)] est corrélé à la [(densité de population) pour certaines (classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...))] ?
import os
import pandas as pd
import json
import re
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

"""clean and split string from insee webpage to extract population age category and number
Input bs4.element.tag : contenu HTML correspondant à une ligne du tableau TrancheAge/Population
Output ['Tranche', total]: ex: [u"3 à 5 ans", u"25 495"]
"""
def extractPopCardinal(popPourUneTrancheAge):
    popPourUneTrancheAgeListe = popPourUneTrancheAge.text.replace(u'\xe0',u'-').split('\n')[1:-1]
    # Tranche, hommes, femmes, ensemble
    #[u'18 - 24 ans', u'42 205', u'42 519', u'84 724']
    return popPourUneTrancheAgeListe[0::3] #On ne retourne que le premier et le dernier élement (tranche, total)

"""Convertit le nombre de population par tranche d'age en densité par tranche d'age pour un departement. On ne recopie pas la tranche (redondant)
Input [['Tranche','total']]: Nombre d'habitants par tranche d'age ex: [[u"3 à 5 ans", u"25 495"],[[u"6 à 10 ans", u"42 484"],...]
Output [0.17,.. 0.31, 1.0] : Densité de population par tranche d'age (dernier élément = total => densité =1)
"""
def fromPopCardinalToDensity(popCardinal):
    total = float(popCardinal[-1][-1].replace(" ",""))
    print "total=",total,"pour ",popCardinal[-1][-1]
    return [float(popPourUneTrancheAge[1].replace(" ",""))/total for popPourUneTrancheAge in popCardinal]

""" Récupère la densité de population par tranche d'age pour un département
Input uString: Index d'un département ('69')
Output [0.17,.. 0.31, 1.0] : Densité de population par tranche d'age
"""
def getPopDensityForOneDepartement(departementIdx):
    #print departementIdx
    url = "http://www.insee.fr/fr/themes/tableau_local.asp?ref_id=POP1A&millesime=2012&niveau=1&typgeo=DEP&codgeo="+departementIdx
    soup = getSoupFromUrl(url)
    densiteTranchesAgeTab = soup.findAll("tbody")[0]
    #densiteTranchesAge = densiteTprintranchesAgeTab.find_all("td")

    popCardinal = [extractPopCardinal(popPourUneTrancheAge) for popPourUneTrancheAge in densiteTranchesAgeTab.find_all("tr")]
    popDensity  = fromPopCardinalToDensity(popCardinal)
    print "pop density:",popDensity
    return popDensity

""" Renvoie une dataframe avec la répartition de la population par département et par tranche d'age
Input Series : Indexes des départements('01','02'...)
Output DataFrame : (départementIdx, Tranches Ages)
"""
def getPopDensity(departementsIdx):
    columns = [u"Moins de 3 ans",u"3 à 5 ans",u"6 à 10 ans",u"11 à 17 ans",u"18 à 24 ans",u"25 à 39 ans",u"40 à 54 ans",u"55 à 64 ans",u"65 à 79 ans",u"80 ans ou plus",u"Ensemble"]
    print [ departementIdx for departementIdx in departementsIdx]
    return pd.DataFrame([getPopDensityForOneDepartement(departementIdx) for departementIdx in departementsIdx], index=departementsIdx, columns=columns)

### 1 Récupération des données sur la densité des médecins par département
dataPath = os.path.dirname(os.path.abspath(__file__)) + '/rpps-medecin-tab7-densite-pointVirgule.csv' #'/Medecin-densite.csv'
data = pd.read_csv(dataPath, encoding="iso-8859-1", skiprows=4).dropna()
#On récupère les départements
departementsIdxBool = data.loc[:,u'SPECIALITE'].str.contains(r'\d{2}') #Masque pour détecter les départements dans le dataset
dataParDepartements = data.loc[departementsIdxBool,:]

#print dataParDepartements.loc[80:,dataParDepartements.columns[0:2]] #debug
#On récupère les données sur les départements (Index et Nom)
departements = pd.DataFrame(dataParDepartements.loc[:,u'SPECIALITE'].str.split(u" - ").tolist(), columns=['index','nom'])
#departements['index'] #Series contenant tous les index des départements (01,02,...,95,971,...,974)
dd = departements['index'][:-1] #On enlève Mayotte, la page Insee existe mais donne des valeurs fausses (=0)
departementsIndexTest = dd.tail(3)

### 2 Récupération des données concernant la densité de population par tranche d'age par département
popDensityTotal = getPopDensity(departementsIndexTest.tolist())

popDensityTotal.head()


#[0.04502220772617826, 0.04866154082288499, 0.08423347371046497, 0.11674285083890525, 0.10159435165910422, 0.1981308097426206, 0.21834919371084868, 0.09602563241656514, 0.07148081885594236, 0.019760319637769443, 1.0]
