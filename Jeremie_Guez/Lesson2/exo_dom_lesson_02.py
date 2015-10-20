import requests
from bs4 import BeautifulSoup


def extractIntFromText(text):
  return float(text.replace(u'\xa0', u''))

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup
  
def getDataFromCss(number):
    colonne_habitant=soup.findAll("td", { "class" : "montantpetit G" })[number].text
    return colonne_habitant

def extractMetricsFromTab(number):
    for element in number:
        colonne_habitant.append(getDataFromCss(tab_number[i]))


def extractMetricsFromUrl(url):
    soup=getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013')
    colonne_habitant=
    
    

    



tab_number_habitant=[1,4,10,13]
tab_number_strate=[2,5,11,14]

colonne_strate=[]
colonne_habitant = []

for i in range (0,len(tab_number)):
    colonne_habitant.append(getDataFromCss(tab_number[i]))
    print(colonne_habitant[i])




#==============================================================================
# getDataFromCss(tab_number)
# 
# colonne_strate_a= soup.findAll("td", { "class" : "montantpetit G" })[2].text
# 
# colonne_habitant_b = soup.findAll("td", { "class" : "montantpetit G" })[4].text
# colonne_strate_b= soup.findAll("td", { "class" : "montantpetit G" })[5].text
# 
# colonne_habitant_c = soup.findAll("td", { "class" : "montantpetit G" })[10].text
# colonne_strate_c= soup.findAll("td", { "class" : "montantpetit G" })[11].text
# 
# colonne_habitant_d = soup.findAll("td", { "class" : "montantpetit G" })[13].text
# colonne_strate_d= soup.findAll("td", { "class" : "montantpetit G" })[14].text
# 
# 
# 
# print(colonne_habitant)
#   
#   
#==============================================================================

