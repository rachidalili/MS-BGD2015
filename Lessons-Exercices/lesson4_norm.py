# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re


credits_cards = ' Thanks for paying with 1098-1203-1233-2354'
cred_regex = re.compile(r'\d{4}-\d{4}$')

res = cred_regex.sub('XXXX-XXXX', credits_cards)

email = '''
Voici le fichier complété et le calendrier et la liste des adresses des élèves (elles ne seront opérationnelles que la semaine prochaine).








 pierre.arbelet@telecom-paristech.fr franCOIS.BLas@telecom-paristech.fr geoffray.bories@telecom-paristech.fr claire.chazelas@telecom-paristech.fr dutertre@telecom-paristech.fr nde.fokou@telecom-paristech.fr wei.he@telecom-paristech.fr anthony.hayot@telecom-paristech.fr frederic.hohner@telecom-paristech.fr yoann.janvier@telecom-paristech.fr mimoune.louarradi@telecom-paristech.fr david.luz@telecom-paristech.fr nicolas.marsallon@telecom-paristech.fr paul.mochkovitch@telecom-paristech.fr martin.prillard@telecom-paristech.fr christian.penon@telecom-paristech.fr gperrin@telecom-paristech.fr anthony.reinette@telecom-paristech.fr florian.riche@telecom-paristech.fr romain.savidan@telecom-paristech.fr yse.wanono@telecom-paristech.fr ismail.arkhouch@telecom-paristech.fr philippe.cayeux@telecom-paristech.fr hicham.hallak@telecom-paristech.fr arthur.dupont@telecom-paristech.fr dabale.kassim@telecom-paristech.fr xavier.lioneton@telecom-paristech.fr sarra.mouas@telecom-paristech.fr jonathan.ohayon@telecom-paristech.fr alix.saas-monier@telecom-paristech.fr thabet.chelligue@telecom-paristech.fr amoussou@telecom-paristech.fr pierre.arbelet@telecom-paristech.fr
'''

pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'

regex_email = re.compile(pattern, flags=re.IGNORECASE)

matches = regex_email.findall(email)

pattern_group = r'([A-Z0-9_%+-]+)\.?([A-Z0-9_%+-]*)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex_email_group = re.compile(pattern_group, flags=re.IGNORECASE)
matches_group = regex_email_group.findall(email)


#dur_regex = r'(\d{0,2}) (hours?)? (\d{1,2}) min'
#res_paris = dur['Paris'].str.extract('(\d{0,2}) (hours?)? (\d{1,2}) min')
#res_paris_not_null = res_paris.dropna()
#myres = res_paris_not_null.applymap(lambda x : int(x))
#myres['total'] = myres['hours']*60 + myres['min']


#MERGE


insee1 = pd.read_csv('base-cc-evol-struct-pop-2011.csv')
insee2 = pd.read_csv('base-cc-rev-fisc-loc-menage-10.csv')

def strip_corse(val):
  return re.sub('(A|B)','0',str(val))

insee2['CODGEO'] = insee2['CODGEO'].apply(strip_corse).astype(int)
