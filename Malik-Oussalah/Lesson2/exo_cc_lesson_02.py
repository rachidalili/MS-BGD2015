#Crawling sur la page Cdiscount récupération lien/nomproduit/prixprod/#
import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
    #Execute q request toward Youtube
    request = requests.get(url)
    #parse the restult of the request
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def extractPostFromPage(url):
    soup = getSoupFromUrl(url)
    # body = soup.find_all('div', {'class': 'content'})
    blocs = soup.find_all('div', {'class': 'prdtBloc'})
    for bloc in blocs:
        title = bloc.find('div',{'class':'prdtBTit'}).text.encode('utf-8')
        html = bloc.find('a').get('href')
        descr = bloc.find('p', {'class': 'prdtBDesc'}).text.encode('utf-8')
        price = bloc.find('span',{'class':'price'}).text.encode('utf-8')
        print "lien : ", html
        print " "
        print "nom : ", title
        print " "
        print "description : ", descr
        print " "
        print "prix : ", price
        print "########## "
        

    return


def start():
    choix = input("Entrer le produit que vous voulez scrapper!")
    choix = str(choix)
    url = "http://www.cdiscount.com/search/10/{}.html".format(choix.replace(" ","+"))
    extractPostFromPage(url)


start()