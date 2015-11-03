# -*- coding: utf-8 -*-
"""
@author: kim
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

def getdetails( soup ):

    lbcparams = soup.findAll('div', {'class' : "lbcParams criterias"})[0]
    marque = lbcparams.find('td', {'itemprop' : "brand"}).renderContents().strip()
    model = lbcparams.find('td', {'itemprop' : "model"}).renderContents().strip()
    annee_model = lbcparams.find('td', {'itemprop' : "releaseDate"}).renderContents().strip()
    #kilometrage = lbcparams.findAll('td', {'itemprop' : "model"}).text
    kilometrage = lbcparams.select('td:nth-of-type(4)')[0].text
    return  marque,model,annee_model,kilometrage

def fromUrltoSoup( url):
    r = requests.get(url,  stream=True)
    return BeautifulSoup(r.text, 'html.parser')

Liste_region =["ile_de_france"]
Entete = ["title", "brand", "model","annee_model","kilometrage","price","category"]
dt_zoe = pd.DataFrame( columns=Entete)
rows_list = []
for r in range(0,len(Liste_region)):
    url = u'http://www.leboncoin.fr/voitures/offres/'+Liste_region[r]+'/?f=a&th=1&q=renault+zo%C3%A9'
    result = fromUrltoSoup( url)
    list_Cars = result.findAll("div", { "class" : "list-lbc" })[0]
    #print list_Cars

    for a in list_Cars.find_all('a', href=True):
        car_infos = a.findAll("div", { "class" : "lbc" })
        for zoe in car_infos:
            title = zoe.findAll("h2", { "class" : "title" })[0].text.strip()
            price = zoe.findAll("div", { "class" : "price" })[0].text.strip()
            category = zoe.findAll("div", { "class" : "category" })[0].text.strip()
            #print title ,' ',price,' ',category,'\n'

        #print "Found the URL:", a['href']
        r = requests.get( a['href'],  stream=True)
        soup = BeautifulSoup(r.text)
        marque, model,annee_model,kilometrage = getdetails(soup)
        rows_list.append( title)
        rows_list.append( marque)
        rows_list.append( model)
        rows_list.append( annee_model)
        rows_list.append( kilometrage)
        rows_list.append( price)
        rows_list.append( category)
        #rows_list.append(r)
        print rows_list
        df_rows_list = pd.DataFrame(rows_list)
        dt_zoe.append(df_rows_list)


print dt_zoe