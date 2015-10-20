# coding: utf8

import requests
from bs4 import BeautifulSoup
import re

for annee in range(2010,2014):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(annee)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    opCouts = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A","TOTAL DES CHARGES DE FONCTIONNEMENT = B","TOTAL DES RESSOURCES D'INVESTISSEMENT = C","TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
    table = []
    for cout in opCouts:
        tdText = soup.find('td', cout = re.compile('.*'+cout+'.*'))
        strateAmount = tdText.previous.previous
        residentAmount = strateAmount.previous.previous.previous
        totalAmount= residentAmount.previous.previous.previous
        strate = strateAmount
        resident = residentAmount
        total = totalAmount   
        ligne=[]
        ligne.append(annee)
        ligne.append(cout)
        ligne.append(strate)
        ligne.append(resident)
        ligne.append(total)
        table.append(ligne)
        print( "Annee".ljust(5)," ".rjust(45),"Par strate".rjust(20),"Par resident".rjust(20),"Total".rjust(20))
        for l in table:
            print(str(l[0]).ljust(5),l[1].rjust(45),l[2].rjust(20),l[3].rjust(20),l[4].rjust(20))            
            
            





