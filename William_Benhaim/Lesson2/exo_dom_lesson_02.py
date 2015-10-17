import requests
from bs4 import BeautifulSoup
def FromTestToInt(txt):
	return int(txt.replace(u'\xa0',u'').replace(' ',''))

def GetSoupFromUrl(url):
	request=requests.get(url)
	return BeautifulSoup(request.text, 'html.parser')

def OnlyLetter(letter,libelle):
	return "= A" in libelle.text and "A +" not in libelle.text and "A - " not in libelle.text	

def InfoForAYear(soup):
	ListedesOperation=[3,7,15,20]
	for ope in ListedesOperation:
		InfosForOperations(ope)

def InfosForOperations(typeOperation):
	InfosAtrouve=[2,3]
	ListeLibelle=soup.findAll( "tr", {"class" : "bleu"})[typeOperation]
	print ListeLibelle.select('td:nth-of-type('+ str(4) + ')')[0].text
	StrEuroParHabitant = ListeLibelle.select('td:nth-of-type('+ str(InfosAtrouve[0]) + ')')[0]
	StrMoyennedelastrate = ListeLibelle.select('td:nth-of-type('+ str(InfosAtrouve[1]) + ')')[0]
	print  'Euros par habitant',FromTestToInt(StrEuroParHabitant.text)
	print 'Moyenne de la strate' , FromTestToInt(StrMoyennedelastrate.text)
	print '#######'


firstYear=2010
LastYear=2013
for year in range(firstYear,LastYear+1):
	print 'year',year
	url='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year)
	soup=GetSoupFromUrl(url)

	InfoForAYear(soup)


#for libelle in {3,7,15,20}:
#print ListeLibellePetit[libelle]
	print '#######'


# EuroParHabitant = str_EuroParHabitanty.select('tr:nth-of-type('+ str(2) + ')')
# ListeLibellePetit=soup.findAll( "td", {"class" : "libellepetit G"})


# for libelle in ListeLibellePetit:
	
# 	if OnlyLetter('A',libelle) :
# 		print libelle
		

# 		}
# 	# 	td:nth-of-type(2){

# 	# 	}
		