# coding: utf-8
__author__ = 'kim'  #inspire du devoir de Guillaume Mohr et Aurelien Galicher


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt


#recuperation et traitement de rpps_tab3.csv

print("###################################traitement du fichier rpps_tab3.csv = nbr medecins par departement / annee/ specialité")
df_med = pd.read_csv("data_cours6/rpps_tab3.csv")
df_med= df_med[df_med['annee'] == 2014]
print df_med.ix[55:65,1]
# récupération du code département.
regx = re.compile(r'([0-9]\w[0-9]?) -')
df_med['dep'] = list(map(lambda x: regx.search(x).groups()[0] if regx.search(x) else None , list(df_med['zone_inscription'].astype(str))))
df_med = df_med.drop('annee',1) #removing annee filtree a 2014
print df_med.head()
df_med= df_med.groupby(['dep','specialite']).sum()
print df_med
df_med = df_med.reset_index()#reindexation dan l ordre
#affichage sous forme tableau croise dynamique avec lignes(index) = dep et colonnes = specialites
pivot_med = df_med.pivot(index='dep', columns='specialite', values='effectifs')
print type(pivot_med)#le resultat est toujours une df
print "pivot: ", '\n',pivot_med.head()

#operation inverse du pivot, on revient au format en 3 colonnes initial
print "pivot_med.stack(): ", '\n'
print pivot_med.stack()

#proportion de specialistes sur tous praticiens et de geriatres sur tous praticiens
pivot_med['r_spe_tot'] = pivot_med['Spécialistes'] / pivot_med['Ensemble des spécialités d\'exercice']
pivot_med['r_ger_tot'] = pivot_med['Gériatrie'] / pivot_med['Ensemble des spécialités d\'exercice']
print pivot_med.head()
#analyse structure de df type pivot
print pivot_med.columns.values #affichage des specialites
print pivot_med.index.values #affichage des departelents
#on observe que les champs affichés : specialite et dep ne sont ni dans les index ni dans les colonnes , informations en plus

#histogramme a corriger pour affichage pour chaque departement, pour le moment les deps sont regroupes par valeur
fig, ax = plt.subplots()
pivot_med['r_ger_tot'].hist(figsize=(16,6), bins=105)
plt.title('repartition du ratio geriatre/ensemble medecin par departement')
plt.show()




# Pour utiliser le fichier de densite des medecins par specialite,
# on telecharge format csv a partir du site http://www.data.drees.sante.gouv.fr/TableViewer/tableView.aspx?ReportId=1155
#on recupere ainsi la fichier rpps-medecin-tab7-densite-2013-14-15-v1_51872514070569
print "###########Chargement fichier rpps des densites de medecin par dep, specialite en colonnes ########################"
rpps = pd.read_csv('data_cours6/rpps-medecin-tab7-densite-2013-14-15-v1_51878339473545.csv',
                    skiprows=[0, 1, 2, 3, 5]) #encoding='latin9', est a eviter a ce moment la car le traitement avec regex ulterieur ne passe plus
# sans preciser le type d'encodage on a des caracteres bizarres : rpps = pd.read_csv('data_cours6/rpps-medecin-tab7-densite-2013-14-15-v1_51878339473545.csv', skiprows=[0, 1, 2, 3, 5])
#on a les infos dabord par region puis si on descend dans le fichier, on les a par departement
rpps.rename(columns={'SPECIALITE': 'ZoneInscription'}, inplace=True)  #renommage d une colonne existante
print " rpps: ",'\n', rpps.ix[:5,:14], '\n','\n'

#ici on veut creer une nouvelle colonne qui contienne les codes de departements
regx = re.compile(r'([0-9]\w[0-9]?) -') #ici on cree le pattern regex que l on va appliquer au cellules de la colonne ZoneIncription
rpps['dep'] = list(map(lambda x: regx.search(x).groups()[0] if regx.search(x) else None , list(rpps['ZoneInscription'].astype(str))))
#df_med.dropna() #removing non dep
print " rpps: ", rpps.ix[36:45,[0,-1]], '\n','\n'
print type(rpps)
print rpps.columns.values
#affichage geriatre par departement
print "affichage geriatre par departement: ",'\n'
rpps_ger = rpps[['G\xe9riatrie','dep']]
rpps_ger = rpps_ger.dropna()
print rpps_ger.head()

####tentative de tranformation en int de la colonne dep
rpps_ger['new_dep'] =  rpps_ger.apply(lambda r: r["dep"] if (r["dep"] != "2A" or r["dep"] != "2B") else 0 , axis = 1)
new_rpps_ger = rpps_ger[['G\xe9riatrie','new_dep']]
#new_rpps_ger['new_dep'] = new_rpps_ger.apply(lambda r: int(r['new_dep']) , axis = 1)

print new_rpps_ger.ix[36:45,:]
fig2, ax = plt.subplots()
new_rpps_ger['G\xe9riatrie'].hist(figsize=(16,6), bins=105)
plt.title('repartition densite de geriatre departement')
plt.show()




print "###########Chargement fichier depassements honoraires par departement########################"
#On dispose aussi dun fichier precisant les depassements dhonoraire par departement
#data = pd.read_csv('Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013' , sheetname ="Specialistes")

data = pd.io.excel.read_excel("data_cours6/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls", sheetname ="Specialistes", na_values = "nc")
#print data.head()
print '\n', '\n', '\n'
data = data[['SPECIALISTES','DEPARTEMENT', 'DEPASSEMENTS (euros)','DEPASSEMENT MOYEN (euros)','NOMBRE DE DEPASSEMENTS', 'EFFECTIFS']]
print "Honoraires: ",'\n',data.head()
print '\n', '\n', '\n'

print "Drop des Nan"
data = data.dropna(subset = ['DEPASSEMENTS (euros)', 'DEPASSEMENT MOYEN (euros)'])
# exemple a prendre si plusierus valeurs a supprimer df[df['Behavior'].str.contains("nt", na=False)]
print data[:15]
print '\n', '\n', '\n'

print data[:5]
print '\n', '\n', '\n'
data = data.groupby(['DEPARTEMENT']).sum()
print data.head()
data = data[['NOMBRE DE DEPASSEMENTS']]
print data.head()

fig3, ax = plt.subplots()
data['NOMBRE DE DEPASSEMENTS'].hist(figsize=(16,6), bins=105)
plt.title('repartition depassements')
plt.show()


print "###########Chargement fichier N201508 des depassements honoraires ########################"
#On charge un deuxieme fichier du sitehttps://www.data.gouv.fr/fr/datasets/depenses-d-assurance-maladie-hors-prestations-hospitalieres-par-caisse-primaire-departement/
#Avec ce fichier on a les depassements d honoraire par specialite mais a cheval entre 2014 et 2015 et on a pas de localisation
dep = pd.read_csv('data_cours6/N201508.csv', encoding='latin9', sep=';',decimal=',',thousands='.',dtype={'dep_mon':float})
print "rep: ",'\n', dep.ix[:5,:], '\n','\n'
print dep.shape
dep['count_dep']= list(map(lambda x: 1 if x > 0 else 0, dep['dep_mon']))
dep.ix[:5,:]
print "dep.shape",dep.shape

