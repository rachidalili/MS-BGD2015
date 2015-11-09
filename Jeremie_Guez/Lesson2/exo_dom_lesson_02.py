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
    data_colonne=soup.findAll("td", { "class" : "montantpetit G" })[number].text
    return data_colonne

years=['2010','2011','2012','2013']


for i in range(0,len(years)):
    print ("Years:",years[i])
    soup=getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+years[i])
    tab_number_habitant=[1,4,10,13]
    tab_number_strate=[2,5,11,14]
    tab_indicateur=['A','B','C','D']
    colonne_strate=[]
    colonne_habitant =[]
    
    print ("Euros per capita:")
    
    for i in range (0,len(tab_number_habitant)):
        colonne_habitant.append(getDataFromCss(tab_number_habitant[i]))
        print (tab_indicateur[i], colonne_habitant[i])

    print ("Average stratum:")
    
    for i in range (0,len(tab_number_strate)):
        colonne_strate.append(getDataFromCss(tab_number_strate[i]))
        print (tab_indicateur[i], colonne_strate[i])
        
    print ("=====")