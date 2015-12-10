# Tested with Python 3.5

# We build a dataframe with the following columns
# Link : weblink to Le Bon Coind
# Model : car's model (life, intens or zen)
# PriceEuros : the price in Euros
# PhoneNumber : the phone number of the seller
# Pro : True if the seller is a professional
# Year : year of the car
# Km : number of KM of the car
# ArgusQuote : the argus' price for the car
# BetterThanArgue : True is Le Bon Coin's price is lower than the argus'
#

# NOTES:
# - when a value is not found, we replace is with NaN
# - phone numbers are taken from the text descripption only. We did not
#   manage to find a simple way to do OCR on the picture provided by Le
#   Bon Coin: google's tesseract makes mistakes in this case (mistakes 6 for 5)


from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import pandas as pd
import re
import requests

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
p = {'txtCaracteres': 'D', 'page':'1', 'affListe':'0', 'affNumero':'0', 'isAlphabet':'1', 'inClauseSubst':'0', 'typeRecherche':'0', 'choixRecherche':'medicament',
        'radLibelle':'2', 'radLibelleSub':'4'}
soup = BeautifulSoup(requests.post(url, data=p).text, 'html.parser')
meds = soup(class_='standart') 
regex = re.compile(r'(DOLIPRANE *[\w+]*) +(\d+[,]*\d*) +(.*), *(\S+)')
sol = {'name':[], 'dosage':[], 'unit':[], 'method':[]} 
for m in meds:
    try:
        print(m.text)
        mat = regex.match(m.text).groups()
        if len(mat) == 4:
            sol['name'].append(mat[0])
            sol['dosage'].append(double(mat[1]))
            sol['unit'].append(mat[2])
            sol['method'].append(mat[3].strip())
    except:
        pass
dat = pd.DataFrame(data=sol)
print(dat)
dat.to_csv('doliprane')
