import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


df = pd.DataFrame(columns=['libelle','dose'])
url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"
params ={'page': 1, 'affliste':0,'affNumero': 0, 'isAlphabet':0, 'inClauseSubst':0, 'typeRecherche':0,'choixRecherche':'medicament','txtCaracteres':'doliprane','btnMedic.x':6,'btnMedic.y':11,'radLibelle':1,'radLibelleSub':4}
r = requests.post(url, data=params)
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.select('.standart'):
	print("----")
	print(a.find('a', {"class":"title"}))
	dose_reg = re.search("([0-9]{1-9})", libelle)
	print(dose_reg)
	if dose_reg:
		dose = dose_reg.group(1)
	print(dose[0])
	df = df.append(pd.Series({'libelle':libelle,'dose':dose}, index=['libelle','dose']), ignore_index=True)
	print(a.text)
print(tabulate(listData, headers=['libelle','dose'], tablefmt='psql'))


#print(r.status_code, r.reason)
#print(r.text + '...')


