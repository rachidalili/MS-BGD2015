# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 23:58:20 2015

@author: florian
"""

# EXO_DOM_LESSON5_Corrélations_médecins_honoraires_densité

import pandas as pd

honoraires = pd.read_excel("Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls",
                           sheetname="Spécialistes",header=0,na_values='nc').dropna()

#travail sur les strings pour matcher avec la table desnite_medecin pour préparer le MERGE
honoraires['SPECIALISTES']=  honoraires['SPECIALISTES'].str[4:]                        
honoraires['DEPARTEMENT']=  honoraires['DEPARTEMENT'].str[:2]+" "+ honoraires['DEPARTEMENT'].str[2:]

densite_medecin = pd.read_excel("rpps-medecin-tab7-densite-2013-14-15-v1_27093426902364.xlsx",skiprows=[0,1,2,3,4], index_col=0)
# on décroise le tableau pour faire passer les labels des colonnes comme valeurs 
densite_medecin_stack = densite_medecin.stack()
densite_medecin_stack=densite_medecin_stack.reset_index()
densite_medecin_stack=densite_medecin_stack.rename(columns={'SPECIALITE':'DEPARTEMENT','level_1':'SPECIALISTES',0:'densité'})


comparatif = pd.merge(honoraires,densite_medecin_stack,on=['DEPARTEMENT','SPECIALISTES'])
print (comparatif.head())