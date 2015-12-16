#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re




# init
url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=year'
years = range(2009, 2014)


def htmlCode (year):
	return requests.get(url.replace('year', str(year))).text.encode('utf-8')

def htmlBox (htmlCode):
	return re.findall('<td class="montantpetit G">(.*?)&nbsp;</td>', htmlCode, re.S) or None



Boxes = {1: "Euros par habitant pour A", 
		 2: "Moyenne de la strate pour A", 
		 4: "Euros par habitant pour B", 
		 5: "Moyenne de la strate pour B",
		 10: "Euros par habitant pour C", 
		 11: "Moyenne de la strate pour C",
		 13: "Euros par habitant pour D", 
		 14: "Moyenne de la strate pour D"}

# Main algorithm
for year in years:
	print str(year)
	htmlText = htmlCode(year)
	datas = htmlBox(htmlText)
	if datas:
		for Box in Boxes:
			print Boxes[numBox] + "\t:\t" + str(datas[Box])
	else:
		print 'il n"y a pas de données pour cette année'
