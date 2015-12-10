# -*- coding: utf-8 -*-
__author__ = 'catherine'

"""
Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique
du dépassement d'honoraires ?
Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les
dépassement d'honoraires ?
Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour
certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?
"""

"""
On choisira comme granularité de territoire le département (plus significatif que la région)

1/ Pour les dépassements d'honoraires sur les praticiens spécialistes :
On dispose d'un jeu de données disponibles sur 2013 : sur le site ameli.fr
ici : http://www.ameli.fr/fileadmin/user_upload/documents/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls
2/ Les données du point 1 étant relatives à 2013, on les mettra en regard des données de densité de 2013 qu'on récupérera
sous format csv à partir de http://www.data.drees.sante.gouv.fr/ReportFolders/reportFolders.aspx?IF_ActivePath=P,490,497,514

Pour les questions de mise en regard de la densité de spécialistes avec la structure de la population par tranche
d'âge, on utilisera les données de l'insee et en particulier le fichier suivant :
http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/estim-pop/estim-pop-dep-sexe-aq-1975-2014.xls
"""

import requests
from bs4 import BeautifulSoup
#import re
#import json
import pandas as pd
import sys
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t
import statsmodels.formula.api as smf


global column_dict
column_dict = {
    'DEPARTEMENT': 'SPECIALITE',
    'TTES_SPECIALITES': 'Ensemble des spécialités d''exercice',
    'SPECIALISTES': 'Spécialistes',
    'ANATOMIE': 'Anatomie et cytologie pathologiques',
    'ANESTHESIE': 'Anesthésie-réanimation',
    'BIOLOGIE': 'Biologie médicale',
    'CARDIOLOGIE': 'Cardiologie et maladies vasculaires',
    'CHIRURGIE': 'Chirurgie générale',
    'STOMATOLOGIE': 'Chirurgie maxillo-faciale et stomatologie',
    'TRAUMATOLOGIE': 'Chirurgie orthopédique et traumatologie',
    'CHIR_INFANT': 'Chirurgie infantile',
    'CHIR_PLASTIQUE': 'Chirurgie plastique reconstructrice et esthétique',
    'CHIR_CARDIO': 'Chirurgie thoracique et cardio-vasculaire',
    'CHIR_UROLOGIQUE': 'Chirurgie urologique',
    'CHIR_VASCULAIRE': 'Chirurgie vasculaire',
    'CHIR_DISGESTIVE': 'Chirurgie viscérale et digestive',
    'DERMATOLOGIE': 'Dermatologie et vénéréologie',
    'ENDOCRINOLOGIE': 'Endocrinologie et métabolisme',
    'GENETIQUE': 'Génétique médicale',
    'GERIATRIE': 'Gériatrie',
    'GYNECOLOGIE': 'Gynécologie médicale',
    'OBSTETRIQUE': 'Gynécologie-obstétrique',
    'HEMATOLOGIE': 'Hématologie',
    'HEPATOLOGIE': 'Gastro-entérologie et hépatologie',
    'MEDECINE_TRAVAIL': 'Médecine du travail',
    'MEDECINE_INTERNE': 'Médecine interne',
    'MEDECINE_NUCLEAIRE': 'Médecine nucléaire',
    'READAPTATION': 'Médecine physique et réadaptation',
    'NEPHROLOGIE': 'Néphrologie',
    'NEURO_CHIRURGIE': 'Neuro-chirurgie',
    'NEUROLOGIE': 'Neurologie',
    'ORL': 'O.R.L et chirurgie cervico faciale',
    'ONCOLOGIE': 'Oncologie option médicale',
    'OPHTALMOLOGIE': 'Ophtalmologie',
    'PEDIATRIE': 'Pédiatrie',
    'PNEUMOLOGIE': 'Pneumologie',
    'PSYCHIATRIE': 'Psychiatrie',
    'RADIOLOGIE': 'Radio-diagnostic et imagerie médicale',
    'RADIO_THERAPIE': 'Radio-thérapie',
    'REANIMATION': 'Réanimation médicale',
    'RECHERCHE': 'Recherche médicale',
    'RHUMATOLOGIE': 'Rhumatologie',
    'MEDECINE_SOCIALE': 'Santé publique et médecine sociale',
    'GENERALISTES': 'Généralistes',
    'MEDECINE_GENERALE': 'Médecine générale'
}

global simple_columns
simple_columns = [
    'DEPARTEMENT',
    'TTES_SPECIALITES',
    'SPECIALISTES',
    'ANATOMIE',
    'ANESTHESIE',
    'BIOLOGIE',
    'CARDIOLOGIE',
    'CHIRURGIE',
    'STOMATOLOGIE',
    'TRAUMATOLOGIE',
    'CHIR_INFANT',
    'CHIR_PLASTIQUE',
    'CHIR_CARDIO',
    'CHIR_UROLOGIQUE',
    'CHIR_VASCULAIRE',
    'CHIR_DISGESTIVE',
    'DERMATOLOGIE',
    'ENDOCRINOLOGIE',
    'GENETIQUE',
    'GERIATRIE',
    'GYNECOLOGIE',
    'OBSTETRIQUE',
    'HEMATOLOGIE',
    'HEPATOLOGIE',
    'MEDECINE_TRAVAIL',
    'MEDECINE_INTERNE',
    'MEDECINE_NUCLEAIRE',
    'READAPTATION',
    'NEPHROLOGIE',
    'NEURO_CHIRURGIE',
    'NEUROLOGIE',
    'ORL',
    'ONCOLOGIE',
    'OPHTALMOLOGIE',
    'PEDIATRIE',
    'PNEUMOLOGIE',
    'PSYCHIATRIE',
    'RADIOLOGIE',
    'RADIO_THERAPIE',
    'REANIMATION',
    'RECHERCHE',
    'RHUMATOLOGIE',
    'MEDECINE_SOCIALE',
    'GENERALISTES',
    'MEDECINE_GENERALE'
]

global column_dict_ameli
column_dict_ameli = {
    'DEPARTEMENT': 'SPECIALITE',
    'TTES_SPECIALITES': 'Ensemble des spécialités d''exercice',
    'SPECIALISTES': 'Spécialistes',
    'ANATOMIE': '37',
    'ANESTHESIE': '02',
    'BIOLOGIE': '38',
    'CARDIOLOGIE': '03',
    'CHIRURGIE': '04',
    'STOMATOLOGIE': ['18', '44', '45'],
    'TRAUMATOLOGIE': '41',
    'CHIR_INFANT': '43',
    'CHIR_PLASTIQUE': '46',
    'CHIR_CARDIO': '47',
    'CHIR_UROLOGIQUE': '16',
    'CHIR_VASCULAIRE': '48',
    'CHIR_DISGESTIVE': '49',
    'DERMATOLOGIE': '05',
    'ENDOCRINOLOGIE': '42',
    'GENETIQUE': '78',
    'GERIATRIE': '34',
    'GYNECOLOGIE': '70',
    'OBSTETRIQUE': ['07', '77', '79'],
    'HEMATOLOGIE': '71',
    'HEPATOLOGIE': '08',
    'MEDECINE_INTERNE': '09',
    'MEDECINE_NUCLEAIRE': '72',
    'READAPTATION': '31',
    'NEPHROLOGIE': '35',
    'NEURO_CHIRURGIE': '10',
    'NEUROLOGIE': '32',
    'ORL': '11',
    'ONCOLOGIE': '73',
    'OPHTALMOLOGIE': '15',
    'PEDIATRIE': '12',
    'PNEUMOLOGIE': '13',
    'PSYCHIATRIE': ['33', '75', '17'],
    'RADIOLOGIE': '06',
    'RADIO_THERAPIE': ['74', '76'],
    'REANIMATION': '20',
    'RHUMATOLOGIE': '14'
}

global ameli_spe_codes
ameli_spe_codes = {
    '37': 'ANATOMIE',
    '02': 'ANESTHESIE',
    '38': 'BIOLOGIE',
    '03': 'CARDIOLOGIE',
    '04': 'CHIRURGIE',
    '18': 'STOMATOLOGIE',
    '44': 'STOMATOLOGIE',
    '45': 'STOMATOLOGIE',
    '41': 'TRAUMATOLOGIE',
    '43': 'CHIR_INFANT',
    '46': 'CHIR_PLASTIQUE',
    '47': 'CHIR_CARDIO',
    '16': 'CHIR_UROLOGIQUE',
    '48': 'CHIR_VASCULAIRE',
    '49': 'CHIR_DISGESTIVE',
    '05': 'DERMATOLOGIE',
    '42': 'ENDOCRINOLOGIE',
    '78': 'GENETIQUE',
    '34': 'GERIATRIE',
    '70': 'GYNECOLOGIE',
    '07': 'OBSTETRIQUE',
    '77': 'OBSTETRIQUE',
    '79': 'OBSTETRIQUE',
    '71': 'HEMATOLOGIE',
    '08': 'HEPATOLOGIE',
    '09': 'MEDECINE_INTERNE',
    '72': 'MEDECINE_NUCLEAIRE',
    '31': 'READAPTATION',
    '35': 'NEPHROLOGIE',
    '10': 'NEURO_CHIRURGIE',
    '32': 'NEUROLOGIE',
    '11': 'ORL',
    '73': 'ONCOLOGIE',
    '15': 'OPHTALMOLOGIE',
    '12': 'PEDIATRIE',
    '13': 'PNEUMOLOGIE',
    '33': 'PSYCHIATRIE',
    '75': 'PSYCHIATRIE',
    '17': 'PSYCHIATRIE',
    '06': 'RADIOLOGIE',
    '74': 'RADIO_THERAPIE',
    '76': 'RADIO_THERAPIE',
    '20': 'REANIMATION',
    '14': 'RHUMATOLOGIE'
}

global pop_columns
pop_columns = [
    'DEP_ID', 'DEPARTEMENT',
    '0_4', '5_9', '10_14', '15_19', '20_24', '25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64',
    '65_69', '70_74', '75_79', '80_84', '85_89', '90_95', '95_et_plus'
]

reload(sys)
sys.setdefaultencoding("utf-8")
sns.set(color_codes=True)

#
# Replace several substrings in string
#
def replace_non_ascii(text):
    dic = {'é': 'e', 'è': 'e', 'ô': 'o'}
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


#
# Chargement dataset des densités de spécialistes
#
def getDensites():
    global simple_columns
    df_densites = pd.read_csv("rpps-medecin-densite-2013.csv", header=35, encoding="iso-8859-1")
    df_densites.columns = simple_columns
    df_densites['DEPARTEMENT'] = df_densites['DEPARTEMENT'].map(replace_non_ascii)
    df_densites['DEPARTEMENT'] = df_densites['DEPARTEMENT'].str.extract("-\ ([A-Z][A-Za-z\ \-']*)")
    df_densites['DEPARTEMENT'] = df_densites['DEPARTEMENT'].str.upper()
    df_densites.index = df_densites['DEPARTEMENT']
    df_densites.drop('DEPARTEMENT', axis=1, inplace=True)
    # Eliminer les colonnes inutiles
    df_densites.drop('MEDECINE_GENERALE', axis=1, inplace=True)
    df_densites.drop('GENERALISTES', axis=1, inplace=True)
    df_densites.drop('MEDECINE_SOCIALE', axis=1, inplace=True)
    df_densites.drop('MEDECINE_TRAVAIL', axis=1, inplace=True)
    df_densites.drop('MEDECINE_INTERNE', axis=1, inplace=True)
    df_densites.drop('TTES_SPECIALITES', axis=1, inplace=True)
    df_densites.drop('RECHERCHE', axis=1, inplace=True)
    return df_densites

def getDepassementsSpe():
    global ameli_spe_codes
    df = pd.read_excel("Honoraires_prof_sante_par_dep_2013.xls", sheetname='Spécialistes',
                       encoding='UTF-8', na_values=['nc'], thousands=' ', keep_default_na=False,
                       skip_footer=4017)
    # remove columns from 2 to 7
    df = df.drop(df.columns[range(2, 8)], axis=1)
    # set columns titles
    df.columns = ['SPECIALITE', 'DEPARTEMENT', 'DEPASSEMENT']
    # select and remove rows with first column begining with TOTAL
    select = df.iloc[:, 0].str.startswith('TOTAL')
    df = df.drop(df[select].index)
    # select and remove rows with second column begin ing with TOTAL
    select = df.iloc[:, 1].str.startswith('TOTAL')
    df = df.drop(df[select].index)
    df = df.reset_index(drop=True)
    df.iloc[:, 1] = df.iloc[:, 1].map(replace_non_ascii)
    df.iloc[:, 1] = df.iloc[:, 1].str.extract("-\ ([A-Z][A-Za-z\ \-']*)")
    df.iloc[:, 1] = df.iloc[:, 1].str.upper()
    # keep only code for SPECIALITE
    df['SPECIALITE'] = df['SPECIALITE'].str[0:2]
    df['SPECIALITE'] = df['SPECIALITE'].map(ameli_spe_codes)
    df.to_csv('dep1.csv')
    grp = df.groupby(['DEPARTEMENT', 'SPECIALITE'])
    depassement_sums = grp['DEPASSEMENT'].sum()
    depassement_sums = depassement_sums.copy()
    df.drop('DEPASSEMENT', axis=1, inplace=True)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    depassement_sums = depassement_sums.reset_index(drop=True)
    df['DEPASSEMENT'] = depassement_sums
    df.to_csv('dep2.csv')
    df.index = df['DEPARTEMENT']
    df.drop('DEPARTEMENT', axis=1, inplace=True)
    return df

#
# Chargement du dataset de données insee sur la structure des populations par département
#
def getPopulationDF():
    global pop_columns
    df = pd.read_excel("estim-pop-dep.xls", sheetname="2013", parse_cols=21, skiprows=4, skip_footer=4)
    df.columns = pop_columns
    df = df.drop([96])
    #df = df.dropna()
    df['DEPARTEMENT'] = df['DEPARTEMENT'].map(replace_non_ascii)
    df['DEPARTEMENT'] = df['DEPARTEMENT'].str.upper()
    df.index = df['DEPARTEMENT']
    df.drop('DEP_ID', axis=1, inplace=True)
    df.drop('DEPARTEMENT', axis=1, inplace=True)
    return df

#
# Récupérer le parsing Soup d'une page HTML accessible via le paramètre url
#
def getSoupFromUrl(url):
    #Execute q request toward Youtube
    request = requests.get(url)
    #parse the restult of the request
    soup = BeautifulSoup(request.text, 'html.parser')
    request.connection.close()
    return soup

def depassement2float(str):
    str = str.replace(",", ".")
    return float(str)

#
# Récupérer les données de dépassement d'honoraires par département
#
def getDepassements(departements):
    soup = getSoupFromUrl("http://www.leciss.org/espace-presse/actualit%C3%A9s/cr%C3%A9ation-de-lobservatoire-citoyen-des-restes-%C3%A0-charge-en-sant%C3%A9")
    data = soup.find_all("p", {'class': 'MsoNormal'})
    # ne conserver que les lignes correspondant à un département
    data = [item for item in data if item.text.endswith('€')]
    result = []
    for d in data:
        parser = d.text.split()
        # ne garder que les lignes correspondant à un département
        lg = len(parser)
        dep = ""
        for i in range(0, lg-2):
            if i == 0:
                dep = parser[i]
            else:
                dep += " "+parser[i]
        # clean SEINE-SAINT-DENIS et ALPES-DE-HAUTE-PROVENCE
        if dep == "SEINE-ST-DENIS":
            dep = "SEINE-SAINT-DENIS"
        elif dep == "ALPES-DE-HTE-PROVENCE":
            dep = "ALPES-DE-HAUTE-PROVENCE"
        if dep in departements.unique():
            result.append([dep, depassement2float(str(parser[lg-2]))])
    result = pd.DataFrame(result, columns=['DEPARTEMENT', 'MOYENNE DEPASSEMENT'])
    result.index = result['DEPARTEMENT']
    result.drop('DEPARTEMENT', axis=1, inplace=True)
    return result

df_densites = getDensites()
#print(df_densites)
data = getDepassementsSpe()
print(data)
print(len(data))
pop = getPopulationDF()
print(pop.head(10))
print
print(pop.shape)
print(df_densites.shape)
print
# merge df_densite et data
df_densites = df_densites.join(data)
df_densites.to_csv("densites_spe.csv")

# corrélation entre densité de spécialistes et dépassements d'honoraires ?
# Calcul d'une régression linéaire sur variable explicative centrée/réduite

df = df_densites.dropna()
X = df.iloc[:, 0]
y = df['MOYENNE DEPASSEMENT']
# centrer/réduire X
mean = X.mean()
std = X.std()
Xcr = (X - mean)/std
dat = pd.concat([Xcr, y-y.mean()], axis=1)
dat.columns = ['DENSITE_SPECIALISTES', 'MOYENNE_DEPASSEMENT']
#print(dat)
#plt.scatter(Xcr, y, c='blue', alpha=0.5)
ax = sns.regplot(x='DENSITE_SPECIALISTES', y='MOYENNE_DEPASSEMENT', data=dat)
plt.show()
ax = sns.residplot(x=Xcr, y=y-y.mean())
plt.show()

#
# Régression linéaire par statmodels
#
result = smf.ols('MOYENNE_DEPASSEMENT ~ DENSITE_SPECIALISTES', data=dat).fit()
print(result.params)
sns.distplot(result.resid, fit=norm)
plt.title('Residuals vs. Normal distribution')
plt.show()
#print(df_densites)

# corrélation entre densité de bébés et de pédiatres
# Calcul d'une régression linéaire sur variable explicative centrée/réduite

df = df_densites
df = df.drop(['MAYOTTE'])
print(df.shape)
print(pop.shape)
X = df[['PEDIATRIE']]
y = pop['0_4']
# centrer/réduire X
mean = X.mean()
std = X.std()
Xcr = (X - mean)/std
dat = pd.concat([Xcr, y-y.mean()], axis=1)
dat.columns = ['DENSITE_PEDIATRES', 'NOMBRE_BEBES']
#print(dat)
#plt.scatter(Xcr, y, c='blue', alpha=0.5)
ax = sns.regplot(x='DENSITE_PEDIATRES', y='NOMBRE_BEBES', data=dat)
plt.show()
ax = sns.residplot(x=Xcr, y=y-y.mean())
plt.show()
