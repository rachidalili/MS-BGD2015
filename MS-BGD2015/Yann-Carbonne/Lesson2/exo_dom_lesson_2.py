#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re

# ============= README =============
# 
# Do NOT use regular expressions to parse HTML at home
# -> http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454
#
# ============ /README =============

# CONFIGURATION
URL = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%YEAR%'
YEARS = range(2009, 2014)


def getHtml (year):
	"""Get the HTML in text for a given year."""
	return requests.get(URL.replace('%YEAR%', str(year))).text.encode('utf-8')

def getBoxes (htmlText):
	"""Get all the boxes' content for a given text of HTML"""
	return re.findall('<td class="montantpetit G">(.*?)&nbsp;</td>', htmlText, re.S) or None


# Num of the box for each data 
matchingBoxes = {1: "Euros par habitant pour A", 2: "Moyenne de la strate pour A", 
				 4: "Euros par habitant pour B", 5: "Moyenne de la strate pour B",
				 10: "Euros par habitant pour C", 11: "Moyenne de la strate pour C",
				 13: "Euros par habitant pour D", 14: "Moyenne de la strate pour D"}

# Main algorithm
for year in YEARS:
	print '\n=========\n  ' + str(year) + '\n========='
	htmlText = getHtml(year)
	results = getBoxes(htmlText)
	if results:
		for numBox in matchingBoxes:
			print matchingBoxes[numBox] + "\t:\t" + str(results[numBox])
	else:
		print 'No data'
