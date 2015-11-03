# encoding: utf-8

import requests
import urllib2
import re
from bs4 import BeautifulSoup
import pandas as pd
from subprocess import call
import random
import time


def retrieve_phone_number_ocr(soup):
    # On lit le code JS executé au clic, et on extrait les paramètres
    # de la seconde requête
    node = soup.find('span', {'id': 'phoneNumber'})
    if node is not None:
        params = re.findall(r'\(.*, (\d+), \"(.+)\"\)', node.find('a')['href'])
        # Appel à l'API de LBC pour récupérer l'url du gif du numéro de téléphone
        print u'   --> extraction du numéro (wait 5 seconds)'
        time.sleep(5)  # 5 seconds
        proxy = 'http://' + proxies.iloc[random.randrange(len(proxies))].values[0]
        print u'   --> extraction du numéro (random proxy): ' + proxy
        r = requests.post(
            'https://api.leboncoin.fr/api/utils/phonenumber.json',
            {
                'list_id': int(params[0][0]),
                'app_id': 'leboncoin_web_utils',
                'key': params[0][1]
            },
            headers={
                'Host': 'api.leboncoin.fr',
                'Origin': 'http://www.leboncoin.fr',
                'Referer': node.url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
            },
            proxies={
                #'https': proxy
            })
        # Si le JSON contient un status OK alors on continue
        # si le status est KO, on vient de se faire bloquer (ça va très vite, malgré le proxy aléatoire)
        print u'   --> extraction du numéro (status): ' + r.json()['utils']['status']
        if r.json()['utils']['status'] == 'OK':
            # On télécharge le gif du numéro et on l'écrit en local
            gif_url = r.json()['utils']['phonenumber']
            f = open('temp.gif', 'wb')
            f.write(requests.get(gif_url).content)
            f.close()
            # Conversion de temp.gif en temp.jpeg
            # nécessite d'être sous OSX
            call(["sips", "-s", "format", "jpeg", "temp.gif", "--out", "temp.jpeg"])
            # OCR du numéro
            # nécessite d'avoir tesseract installé
            call(["tesseract", "temp.jpeg", "temp", "-psm", "7", "nobatch", "digits"])
            # On lit la sortie de l'OCR
            numero = open('temp.txt').read()
            if len(numero) > 0:
                return re.sub(r'\D', '', numero)
            else:
                # L'OCR a merdé, pas de numéro
                return None
        else:
            return None
    else:
        return None


def retrieve_phone_number_desc(soup):
    desc = soup.find('div', {'itemprop': 'description'})
    phone_numbers = re.findall(r'((?:\d[\s\.-]?){10})', desc.get_text())
    if len(phone_numbers) > 0:
        return re.sub(r'\D', '', phone_numbers[0])
    else:
        return None


def retrieve_version(soup):
    titre = soup.find('h1', {'itemprop': 'name'}).get_text().lower()
    version = None
    for v in versions:
        if v in titre:
            version = v
            break
    return version


def retrieve_year(soup):
    annee = soup.find('td', {'itemprop': 'releaseDate'})
    if annee is not None:
        return int(re.sub(r'\D', '', annee.get_text()))
    else:
        return None


def retrieve_kilometers(soup):
    kilometrage = None
    for c in soup.find('div', {'class': 'lbcParams criterias'}).findAll('tr'):
        if u'Kilométrage' in c.find('th').get_text():
            kilometrage = int(re.sub(r'\D', '', c.find('td').get_text()))
            break
    return kilometrage


def retrieve_price(soup):
    prix = soup.find('span', {'class': 'price'})
    if prix is not None:
        return float(re.sub(r'\D', '', prix.get_text()))
    else:
        return None


def retrieve_pro(soup):
    pro = soup.find('span', {'class': 'ad_pro'})
    return pro is not None



urls_lbc = [
    "http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&fu=4&q=zoe&it=1",
    "http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?f=a&th=1&fu=4&q=zoe&it=1",
    "http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&fu=4&q=zoe&it=1"
]
versions = ['intens', 'zen', 'life']
annees = [2012, 2013, 2014]

data_lbc = pd.DataFrame(columns=['Version', 'Année', 'Kilométrage', 'Prix', 'Téléphone', 'Pro'])
data_cote = pd.DataFrame(columns=['Année', 'Version', 'Cote'])

proxies = pd.read_csv('_reliable_list.txt')


for url in urls_lbc:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ads = soup.findAll('div', {'class': 'lbc'})
    for ad in ads:
        ad_url = ad.parent['href']
        print 'Annonce: ' + ad_url
        r = requests.get(ad_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        data_lbc = data_lbc.append({
            'Version': retrieve_version(soup),
            'Année': retrieve_year(soup),
            'Kilométrage': retrieve_kilometers(soup),
            'Prix': retrieve_price(soup),
            'Téléphone': retrieve_phone_number_desc(soup),
            'Pro': retrieve_pro(soup)
        }, ignore_index=True)


url_cote = "http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide-{annee}.html"

for annee in annees:
    for version in versions:
        url = url_cote.replace('{version}', version)
        url = url.replace('{annee}', str(annee))
        print 'Cote: ' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        cote = float(re.sub(r'\D', '', soup.find('span', {'class': 'Result_Cote'}).get_text()))
        data_cote = data_cote.append({
            'Version': version,
            'Année': annee,
            'Cote': cote
        }, ignore_index=True)

# Inner join sur Version et Année
data_merged = pd.merge(data_lbc, data_cote, on=['Version', 'Année'], how='inner')
data_merged['Delta'] = (data_merged['Prix'] - data_merged['Cote']) / data_merged['Cote'] * 100.
data_merged = data_merged.sort(columns=['Delta'])
data_merged = data_merged.reset_index()
data_merged['Delta'] = data_merged['Delta'].map('{:,.1f}%'.format)
data_merged.to_csv('zoe.csv', sep='\t')

print data_merged
