# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 16:14:40 2015
def deb (x) :
    a = 0
    while (a < x): # (n'oubliez pas le double point !)
        a = a + 1     #pd.read_csv(Emplacement+'R201402_sanslib.CSV', sep=';',  decimal=',',thousands='.', dtype={'dep_mon':float}) (n'oubliez pas l'indentation !)
    return a

deb (10)
@author: bibiane
"""
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

Emplacement="C:/Users/bibiane/Desktop/Santes/"
data_path = "data/R_2014_sans_lib/"
"""

TypeError: cannot concatenate 'str' and 'list' objects,
j avais concaténer emplacement qui est un string avec une liste """

liste = ['0'+str(i) if i <10 else str(i) for i in range(10,13)]
fichiers = [ "R2014"+x+"_sanslib.CSV" for x in liste]
fichierR_df = pd.concat([ pd.read_csv(Emplacement+fichier, sep=';', decimal=',',thousands='.',usecols=[0,17], dtype={'dep_mon':float}) for fichier in fichiers])

