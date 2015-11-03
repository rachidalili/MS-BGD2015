# coding: utf8
"""
Ce script va récupérer des informations sur le doliprane sur une base de données publique de médicaments
"""
import pandas as pd
import json
import re
import requests
from bs4 import BeautifulSoup

"""
Effectue une requête sur une base de données publique de médicaments
Arguments:
 - drug: médicament à analyser
 - page: indice de la page demandée
Retour:
 - soup: une soupe de médicaments... miam miam !
"""
def getSoupOfDrugRequest(drug, page):
    #headers = {'content-type': 'text/html'}
    url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
    data = {
    'choixRecherche':"medicament",
    'page':int(page),
    'affliste':1, #vaut 1 si le clique provient des indices de page 'page 2' sinon vaut 0 si clic depuis page accueil
    'affNumero':0,
    'isAlphabet':0,
    'inClauseSubst':0,
    'nomSubstances':"",
    'btnMedic.x': '12',
    'btnMedic.y': '5',
    'btnMedic': 'Rechercher',
    'typeRecherche':0,
    'txtCaracteres':drug,
    'radLibelle':2,
    'txtCaracteresSub':"",
    'radLibelleSub':4
    }
    response = requests.post(url, data) #A verifier que les headers fonctionnent
    return BeautifulSoup(response.text,'html.parser')

"""
Renvoie les liens correspondant potentiellement aux médicaments (les liens vers les autres pages sont également présents)
Argument> soup: Soupe dans laquelle chercher
Retour  > bs4.ResultSet contenant les liens. Cet objet est une sous-classe de list(). On peut donc le concaténer de la même manière (L1 + L2 ou L1.extend(L2))
"""
def getLiensFromSoup(soup):
    return soup.findAll(attrs={'class':'standart'})

#Première requête
soup = getSoupOfDrugRequest("doliprane", 1)

#On récupère le nombre de pages. Pour afficher les autres pages il faut effectuer une requête post en mettant à jour le param page
pageCountRaw = soup.findAll('div',{'class':'navBarGauche'})[0].text
pageCount    = re.compile(r'(\d+)$').search(pageCountRaw).group()

#On récupère à partir de toutes pages, tous les liens correspondant potentiellement à des médicaments
links = list()
[links.extend(getLiensFromSoup(soup)) for soup in [getSoupOfDrugRequest("doliprane", page) for page in xrange(1,int(pageCount)+1)]]

#On récupère uniquement les liens correspondant à des médicaments et on stocke dans un dataframe le contenu brut
drugsRawData =  pd.DataFrame([link.text for link in links if link['href'].startswith('extrait.php?specid')], columns=[u"rawData"])

#On extrait 3 colonnes des données (Médicament/Poids/Forme Gallénique)
drugsDataInTreatement = pd.DataFrame(drugsRawData["rawData"].str.findall(r"^([A-Z\s]+)(.*),(.+)[\t+]$").tolist())
drugsData = pd.DataFrame(drugsDataInTreatement[0].tolist(), columns=[u'Drug name',u'Weight',u'Dosage form'])

#To Do:
#Trouver un moyen élégant de supprimer les \t
#re.sub('\t','',drugsRawData["rawData"][0]) ?


#Historique:

# Première façon de se débarasser des liens hors sujets vers les autres pages
# Structure des données: une series de listes de tuple (un tuple de 3 champs contenu dans une liste d'un élément)
# Supprimer le dernier champs correspondant au lien vers les autres pages
# On convertit sa ligne en NaN qu'on supprime avec dropna
# str[0] appelle le premier élément de la liste (il n'y en a qu'un)
# str[0,1 ou 2] appelle les éléments du tuple contenus dans la liste (il y en a 3)
#pd.DataFrame({'a': dataMeds.str[0].str[0], 'b': dataMeds.str[0].str[1], 'c': dataMeds.str[0].str[2]}).dropna()

# Deuxième façon:
# Faire un meilleur préprocessing lors du scraping
# On teste sur le contenu de href.Les liens pointant vers les pages descriptives des médicaments commencent par extrait.php, celles vers les autres pages de
#results =  pd.DataFrame([lien.text for lien in liens if lien['href'].startswith('extrait.php?specid')], columns=[u"rawDrugs"])
