import requests
from bs4 import BeautifulSoup
import re


column = ['unité mg']


url = "http://base-donnees-publique.medicaments.gouv.fr/index.php/"
params = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0, 'inClauseSubst': 0,
          'typeRecherche': 0, 'choixRecherche': 'medicament', 'txtCaracteres': 'Doliprane',
          'btnMedic.x': 11, 'btnMedic.y': 10, 'btnMedic': 'Rechercher', 'radLibelle': 2,
          'radLibelleSub': 4}


answer = requests.post(url, data=params)
soup = BeautifulSoup(answer.text)

table = soup.findAll('table')


for div in soup.findAll('a', class_='standart'):
    text = div.get_text()
    print(text)
    try:
        dose = int(re.findall('[0-9]{3,4}', text)[0])
    except IndexError:
        dose = float(re.findall('[0-9]{1,2},[0-9]{1,2}', text)[0].replace(",", "."))

    #unit = re.findall('^*\d\s,', text)
    # print(unit)
    print(dose)

    forme = re.findall(',.*$', text)[0].replace("\t", "").replace(",", "").strip()
    print(forme)
