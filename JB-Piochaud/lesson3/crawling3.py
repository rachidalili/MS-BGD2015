# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:39:31 2015

@author: jean-baptiste
"""

import requests
import re

URL = 'http://www.cdiscount.com/ct-ordinateurs-portables/acer+aspire.html#_his_'

"""def getUrl(url):
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup"""
  
def getHtml(url):
	"""Get the HTML in text for a given year."""
	return requests.get(url).text.encode('utf-8')
  
def getTitle(htmlText):
    return re.findall('<div class="prdtBTit">', htmlText, re.S) or None
    
#def getNewPrice():
    
    
#def getOldPrice():
    
htmlText = getHtml(URL)    
Title = getTitle(htmlText)
