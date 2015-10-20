# coding: utf8

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
  #Execute q request toward url
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def extractCdiscountData(url):

  uneFicheProduit = {}
  fichesProduits = []

  soup = getSoupFromUrl(url)
  blocsProduits = soup.findAll("div", { "class" : "prdtBloc" })
  
  for blocProduit in blocsProduits:
      uneFicheProduit['titre'] = blocProduit.find('div', {'class':'prdtBTit'}).text
      uneFicheProduit['imgSrc'] = blocProduit.find("ul", {"class": "prdtBPCar"}).find("img")['src']
      uneFicheProduit['prixBarre'] =  blocProduit.find('div', {'class': 'prdtPrSt'})
      uneFicheProduit['prix'] = blocProduit.find('span', {'class': 'price'}).get_text()
      fichesProduits.append(uneFicheProduit.copy())
      
  return fichesProduits
   
      
urlAcer = "http://www.cdiscount.com/search/10/acer+aspire.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets=f%2F6%2Facer&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SubSearchFacet=&FacetForm.SubSearchLastOpIsClickOk=&SortForm.SelectedSortLastEvent=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=acer%2Baspire&&_his_"
urlDell = "http://www.cdiscount.com/search/10/dell+xps+15.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets=f%2F6%2Fdell&FacetForm.SubSearchFacet=&FacetForm.SubSearchLastOpIsClickOk=&ProductListTechnicalForm.Keyword=dell%2Bxps%2B15&&_his_"
acer = extractCdiscountData(urlAcer)
dell = extractCdiscountData(urlDell)
print acer