__author__ = 'kim'


import statsmodels.api as sm
import numpy as np
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup

#Creation de vecteurs et de matrices
print('Creation de vecteurs et de matrices')
res = np.logspace(2.0, 3.0, num=4)
#array([  100.        ,   215.443469  ,   464.15888336,  1000.        ])
print res,'\n'
res = np.logspace(2.0, 3.0, num=4, endpoint=False)
#array([ 100.        ,  177.827941  ,  316.22776602,  562.34132519]) stop is the final value of the sequence, unless endpoint is False. In that case, num + 1 values are spaced over the interval in log-space, of which all but the last (a sequence of length num) are returned.
print res,'\n'
res = np.logspace(2.0, 3.0, num=4, base=2.0)
#array([ 4.        ,  5.0396842 ,  6.34960421,  8.        ])
print res,'\n'

print np.log10(1e-3),'\n'
alphas = np.logspace(np.log10(1e1), np.log10(1e-3), num=10)
print alphas,'\n'
#meme chose que:
alphas = np.logspace(1, -3, num=10)
print alphas,'\n'


#selection d'indices avec conditions sur des valeurs
print('selection d indices')
vector = 0.5*1e-12*np.ones(10)
print vector
vector[:4]+= 2
print vector
indexes_to_keep = np.where(np.abs(vector) > 1e-12)[0]
print indexes_to_keep, '\n'


#Somme des elements d'une matrice
print('Somme des elements d une matrice')
res = np.sum([[0, 1], [0, 5]], axis=0) #ici on somme les elements contenus dans les colonnes, colonnes par colonnes
# resultat : array([0, 6])
print res


# Manipulation des shape
print'Manipulation des shape','\n','\n','\n'
vect = np.random.randn(4,6)
print vect
n_samples = vect.shape[0]
print n_samples


#creation dataframe
print'*******************Creation et manipulation de dataframe**************************','\n'
table_theta = pd.DataFrame(
    columns=(
        'Theta0',
        'Theta1',
        'Theta2',
        'Theta3',
        'Theta4',
        'Theta5'))
print "table theta:"
print table_theta
#affichage de colonnes et drop de colonnes dans dataframe
print '\n','\n','Drop de champs dans dataframe'
url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/datasets/cars.csv'
dat = pd.read_csv(url)
print 'dat[0:15]','\n' , dat[0:15]
print 'dat[\'dist\'][0:15]','\n', dat['dist'][0:15]
#Pour afficher quelques colonnes et choisir aussi les lignes on peut aussi faire
d =  dat[['dist','speed']]
print d[2:15]


print '\n',"emploi de ix, on utilise les index de lignes et de colonnes:"
print 'dat.ix[:5,0:2]','\n', dat.ix[:5,0:2] # Ici comme un tableau mais il faut utiliser ix . Remember that Python does not slice inclusive of the ending index, prend les colonnes de 0 a 1
print '\n','dat.ix[[1,3,4],0:2]','\n', dat.ix[[1,3,4],0:2]


print '\n',"emploi de loc, on utilise les noms de colonnes et idex des lignes"
X = dat
row_indexer = [2,3,4]
column_indexer = ['speed','dist']
print 'X shape: ', X.shape
print X.loc[row_indexer,column_indexer]
print X.loc[2:4,column_indexer]

print '\n',"emploi de iloc, on utilise les noms de colonnes et idex des lignes, revient au meme que ix, privilegier ix"
X = dat
it =5
print 'X.iloc[0:it=5,0]: ','\n',X.iloc[0:it, 0:2]


#Le drop de colonnes
X = dat.drop(['dist', 'Unnamed: 0'], axis=1) #axis = 1 for column, ici j'elimine les colonnes dist et Unnamed
print '\n','X.head() after columns suppression: ','\n', X.head()

#dataframe column slicing, selection de colonnes dans une dataframe
rpps_ger = rpps[['G\xe9riatrie','dep']]

#Ajouter une ligne a une dataframe
X1 = dat.head()
print 'X1:' , X1,'\n', 'shape de X1:', X1.shape
X1.loc[5] = [0 for n in range(3)] #cela ne fonctionne pas car on ne peut ecrire sur une vue d'une dataframe, il faut faire une copie
X1 = X1.copy()
X1.loc[5] = [0 for n in range(3)]
print 'X1:' , X1

df = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
for i in range(5):
        df.loc[i] = [random.randint(-1,1) for n in range(3)]

print df

#ajouter une colonne a une dataframe
print "df avec une nouvelle colonne: ",'\n'
df['nouvelle_col'] = df.apply(lambda r: 1, axis = 1)
print df

#Supprimer des lignes contenant certains champs dans une dataframe
#d abord essayer d'indiquer les valeurs que je en veux pas au moment de l'import csv ou excel par l'attribut na_values = "nc"
dat = sm.datasets.get_rdataset('airquality').data
dat1 = dat.copy()
print dat.head()
dat = dat.dropna(subset = ['Ozone', 'Solar.R'])
print 'dat ss Nan: ','\n',dat.head()


print '\n',dat1.head()
dat1 = dat1.dropna()
print 'dat1 ss Nan: ','\n',dat1.head()

dat2 = dat.drop(dat.index[dat.Temp == 74])
print '\n','dat2: ','\n', dat2.head()


#creer une data frame a partir d'une liste
listInfo=['Region','Version','Annee','Type de Vendeur','Telephone','KM','Prix','Cote','Comparaisan Prix vs Cote']
listregion=['ile_de_france','aquitaine','provence_alpes_cote_d_azur']
listcar=[]
for str_name_region in listregion:
    url='http://www.leboncoin.fr/voitures/offres/'+str_name_region+'/?f=a&th=1&ps=14&q=renault+zoe'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    bloc_all_cars= soup.find('div', { 'class' : 'list-lbc' })
    cars = bloc_all_cars.findAll('a')
    for car in cars:
		url_zoe=car['href']
		listcar.append([str_name_region, 'one','two'])


listALL = listcar
print listALL[0:5]
Result_DF = pd.DataFrame(listALL, columns=['region', 'region1','region2'])
print Result_DF.head()


#################################Modification de data Frame#################################

#####creation de nouvelle colonne a partir d operations sur les precedentes#######################
#exemple de creation d une colonne age a partir de colonne annee de naissance par fonction lambda
#df["ageH"] = df.apply (lambda r:  2014 - int(r["ANAISH"]), axis=1)
#df["ageF"] = df.apply (lambda r:  2014 - int(r["ANAISF"]), axis=1)



#################################Regular expressions#########################################

import re

#######################re.search#######################
patterns = [ 'this', 'that' ]
text = 'Does this text match the pattern?'

for pattern in patterns:
    print 'Looking for "%s" in "%s" ->' % (pattern, text),

    if re.search(pattern,  text):
        print 'found a match!'
    else:
        print 'no match'

##############################re.compile#########################################################
# Pre-compile the patterns
#regexes are regex objects (and have methods like classes)
regexes = [ re.compile(p) for p in [ 'this',
                                     'that',
                                     ]
            ]
text = 'Does this text match the pattern?'

for regex in regexes:
    print 'Looking for "%s" in "%s" ->' % (regex.pattern, text),

    if regex.search(text):
        print 'found a match!'
    else:
        print 'no match'

