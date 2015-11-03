from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import re
import urllib2

url = "http://www.leboncoin.fr/voitures/876165732.htm?ca=21_s" 
col = ['annee','kilometrage', 'prix','telephone','prix_argus']
df = pd.DataFrame(columns=col)


class bon_coin:
    @staticmethod
    def prix_ags(argus_url):    
        html = urllib2.urlopen(argus_url).read()
        soup_3 = BeautifulSoup(html, 'html.parser')
        #print soup
        prix = soup_3.find('span',{'class':'Result_Cote arial tx20'})
        return prix.next
    @staticmethod
    def get_info(url):
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        #print soup
        soup_1 = soup.find('div',{'class':'lbcParamsContainer floatLeft'})
        prix = soup_1.find('tr',{'class':'price'}).find('span',{'class':'price'}).get_text()
        #print price
        soup_2 = soup.find('div',{'class':'lbcParams criterias'})
        #print soup_2
        marque_voiture = soup_2.select("table > tr:nth-of-type(1)")  #[0].find('td').get_text()  > tr:nth-of-type(0)
        type_voiture = soup_2.select("table > tr:nth-of-type(2)")
        kilometrage = soup_2.select("table > tr:nth-of-type(3)")[0].find('td').get_text()
        annee = soup_2.find('td',{'itemprop':'releaseDate'}).get_text()
        annee = annee.strip()
        description = soup.find_all('div',{'class':'content'})
        description = str(description)
        description = description.replace(" ","") # remove white spaces
        res = re.search('[0-9]\d{9}',description) #select number with regx
        if res is None:
            telephone = "null found"
        else:
            telephone = res.group(0)

        items = soup.find("h1",{"itemprop":"name"})
        car_type = items.next
        car_type = unicodedata.normalize('NFKD', car_type).encode('ascii','ignore')
        print car_type
        car_type = str(car_type)
        car_type = car_type.strip()
        zen = re.search('zen',car_type,re.IGNORECASE)
        life = re.search('life',car_type,re.IGNORECASE)
        intens = re.search('intens',car_type,re.IGNORECASE)
        
        items = soup.find("td",{"itemprop":"releaseDate"})
        date = items.next
        date = str(date)
        date = date.strip()
        if zen is None and life is None and intens is not None:
            intens = intens.group(0)
            argus_url = "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-"+date+".html"
            prix_arg = bon_coin.prix_ags(argus_url)
        if zen is None and life is not None and intens is None:
            life = life.group(0)
            
            argus_url = "http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide-"+date+".html"
            print argus_url
            prix_arg = bon_coin.prix_ags(argus_url)

        if zen is not None and life is None and intens is None:
            zen = zen.group(0)
            argus_url = "http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide-"+date+".html"
            prix_arg = bon_coin.prix_ags(argus_url)

        if zen is None and life is None and intens is None:

            prix_arg = "argus is not mentionned"

        #print res.group(0)

        row = [annee,kilometrage,prix,telephone,prix_arg]
        return row
    
def process_row(row):
    print row[1]
    row[1] =  str(row[1])
    row[1] = row[1].replace("KM","")
    row[1] = row[1].replace(" ","")
    row[1] = float(row[1])
    #print row[1]

    row[2] = unicodedata.normalize('NFKD', row[2]).encode('ascii','ignore')  # remove euro caracter
    row[2] = row[2].replace(" ", "")   # remove white space
    row[2] = float(row[2])   # convert to float
    return row

df = pd.DataFrame(columns=col)
def pages(url,df):
    #url = "http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?f=a&th=1&q=renault+zo%C3%A9" 
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')


    soup = soup.find("div", {"class": "list-lbc"})
    list_annonces = soup.find_all('a',href=True)

    for el in list_annonces:
        link = el['href']
        instance = bon_coin()
        row = instance.get_info(link)
        row = process_row(row)
        df2 = pd.DataFrame([row], columns=col)
        df = df.append(df2)
    return df
        
url = "http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?f=a&th=1&q=renault+zo%C3%A9" 
df = pages(url,df)
url = "http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&q=renault+zo%C3%A9"
df = pages(url,df)
url = "http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&q=renault+zo%C3%A9"
df = pages(url,df)
print df
print df.shape
