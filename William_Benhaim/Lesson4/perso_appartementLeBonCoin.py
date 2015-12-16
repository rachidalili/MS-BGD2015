# coding: utf8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def FromTestToInt(txt):
   	return int(txt.replace(u'\xa0', u'').replace(u'\u20ac', u'').replace(' ',''))


def GetSoupFromUrl(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')

def recupKM(txt):
	return int(txt.replace(u'KM', u'').replace(u'\nKilom\xe9trage :', u'').replace(' ',''))

def coteLacentrale(modele,annee):
	url_cote='http://www.lacentrale.fr/cote-auto-renault-zoe-'+modele+'+charge+rapide-'+annee+'.html'
	soupCoteArgus = GetSoupFromUrl(url_cote)
	Cote = soupCoteArgus.find('span', {'class': 'Result_Cote arial tx20'})
	return FromTestToInt(Cote.text)

def getvalueforAttribut(att,param):
	i=1
	
	while not(att in ((param.select('tr:nth-of-type('+str(i)+')'))[0].text).encode('utf-8')):
		print i
		i+=1	

	return filter(None,param.select('tr:nth-of-type('+str(i)+')')[0].text.encode('utf-8').split('\n'))[1].split(' ')[0]

def GetInformation(url_appart):

	listinfo=[]
	soupInfo = GetSoupFromUrl(url_appart)
	print url_appart
	des = soupInfo.find('div', {'itemprop': 'description'})
	pro = soupInfo.find('div', {'class': 'upload_by'})
	pro2 = pro.find('span', {'class': 'ad_pro'})
	
	if pro2 is not None:
	    typevendeur = 'Pro'
	else:
	    typevendeur = 'Perso'
	print typevendeur
	listinfo.append(typevendeur)
	param = soupInfo.find('div', {'class': 'lbcParams criterias'})
	print getvalueforAttribut('Piéce',param)
	
	prix = FromTestToInt(soupInfo.find('span', {'class': 'price'}).text)
	
	# if annee in range(2012,2015) and version is not None:
	# 	cote=(coteLacentrale(version,str(annee)))
	# 	if cote>prix:
	# 		CompareCoteToprice='low'
	# 	else:
	# 		CompareCoteToprice='high'
	# else:
	# 	cote='NA'
	# 	CompareCoteToprice='NA'
	expression = r"0[0-9]([ .-/]?[0-9]{2}){4}"
	#phone=re.search(expression,des)

	isphone= re.search(expression,str(des))
	if isphone:
		phone=isphone.group()
		phone = re.sub(r'\D', "", phone)  
	else:
		phone='NA'
	return ''#str_name_region,version,annee,typevendeur,phone,km,prix,cote,CompareCoteToprice


	

def leBonCoinappart(listDep,args):
	listappart=[]
	region='ile_de_france'
	for lieux in listDep:
		ville,dep=lieux.split(' ')
		strargs=''.join(args)
		url='http://www.leboncoin.fr/ventes_immobilieres/offres/'+region+'/?f=a&th=1'+strargs+'&location='+ville+'%20'+dep

		
		soup = GetSoupFromUrl(url)
		
		bloc_all_appart= soup.find('div', { 'class' : 'list-lbc' })
		if bloc_all_appart is None:
			continue
		appartements = bloc_all_appart.findAll('a')
		expression = r"account"
		#phone=re.search(expression,des)

		
		for appart in appartements:

			
			titleappart = appart['title'].encode('utf-8')
			urlappart = appart['href']
			if not re.search(expression,str(urlappart)):
				listappart.append(GetInformation(urlappart))

	return ''

def plusProche(valeur,listval):

	if valeur =='':
		return ''
	for i in range(len(listval)):
	
		if valeur==listval[i]:
			return i
		else:
			if (valeur>listval[i] and valeur<listval[i+1]):
				return i #if valeur <(listval[i]+listval[i+1])/2 else (i+1)

listInfo=['Region','Version','Annee','Type de Vendeur','Telephone','KM','Prix','Cote','Comparaisan Prix vs Cote']
Surface=['60','80']
ListPrix=[0,25000,50000,75000,100000,125000,150000,175000,200000,225000,250000,275000,300000,
				325000,350000,400000,450000,500000,550000,600000,650000,700000,800000,900000,1000000,
				1100000,1200000,1300000,1400000,1500000,2000000]
ListSurface=[0,20,25,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150,200,300,400,500]


prixinf=500000
prixsup=534000
surfaceinf=80
surfacesup=''
args=[]


args.append('&ps='+str(plusProche(prixinf,ListPrix)) if not plusProche(prixinf,ListPrix) =='' else '')
args.append('&pe='+str(plusProche(prixsup,ListPrix)) if not plusProche(prixsup,ListPrix) =='' else '')
args.append('&sqs='+str(plusProche(surfaceinf,ListSurface)) if not plusProche(surfaceinf,ListSurface) =='' else '')
args.append('&sqe='+str(plusProche(surfacesup,ListSurface)) if not plusProche(surfacesup,ListSurface) =='' else '')

listDep=['Paris 75008','Paris 75009','Paris 75017']
listALL=leBonCoinappart(listDep,args)

#Result_DF = pd.DataFrame(listALL, columns=listInfo)

