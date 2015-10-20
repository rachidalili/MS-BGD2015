# La liste des matériels dispo [Dell XPS 15'', Acer aspire'] sur CDiscount :
# récupérer description de l'article, son prix (nouveau et ancien), lien vers l'image, url de l'article
#

import requests
import pandas as pd
from bs4 import BeautifulSoup

def getPage(words):
    """
    """
    words = "+".join(words)
    url_base = 'http://www.cdiscount.com/search/10/' + words + '.html'
    r = requests.get(url_base)
    return r.text

def resultsProduct(words):
    """Returns the results for a product"""
    soup = BeautifulSoup(getPage(words), 'html.parser')
    gl = []
    for p in soup.select('.prdtBloc'):
        l = []
        
        l.append(p.select('.prdtBTit')[0].text)        
        l.append(p.select('.price')[0].text)
        try:
            l.append(p.select('.prdtPrSt')[0].text)
        except IndexError:
            l.append("")
        l.append(p.select('.jsQs')[0]['href'])
        l.append(p.select('.prdtBImg')[0]['src'])
        gl.append(l)    
    df = pd.DataFrame(data=gl, columns=['Name','Price','OldPrice','URL','ImageURL'])
    print(df)
    return 

def main():
    resultsProduct(['acer', 'aspire'])
    resultsProduct(['dell', 'xps', '15'])
	

if __name__ == '__main__':
    main()
