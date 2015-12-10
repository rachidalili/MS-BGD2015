# -*- coding: utf-8 -*-
from docutils.nodes import danger

__author__ = 'catherine'
#
# générer un fichier de données sur le prix des Renault Zoé sur
#  le marché de l'occasion en Ile de France, PACA et Aquitaine.
# Le fichier doit être propre et contenir les infos suivantes :
# version ( il y en a 3), année, kilométrage, prix, téléphone du
# propriétaire, est ce que la voiture est vendue par un professionnel
#  ou un particulier.
# Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous
# récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.
#

global proxies
proxies = {
  "http": "127.0.0.1:3128",
  "https": "127.0.0.1:3128",
}

#
# Requête générale pour retrouver toutes les Renault Zoe en vente en IDF:
#  http://www.leboncoin.fr/voitures/offres/ile_de_france/?f=a&th=1&q="Renault+Zoe&it=1"
# Requête générale pour retrouver toutes les Renault Zoe en vente en PACA:
#  http://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?f=a&th=1&q=%22Renault+Zoe&it=1
# Requête générale pour retrouver toutes les Renault Zoe en vente en Aquitaine:
#  http://www.leboncoin.fr/voitures/offres/aquitaine/?f=a&th=1&q=Renault+Zoe&it=1

import requests
from bs4 import BeautifulSoup
import re
import json
from PIL import Image
import pyocr
import pyocr.builders
import sys
import random
import time
import pandas as pd

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

url_prefix1 = "http://www.leboncoin.fr/voitures/offres/"

url_prefix2 ="http://www.lacentrale.fr/cote-auto-renault-zoe-"

#
# Pour récupérer les images dans lesquelles sont inscrites les num de tel
# des vendeurs du bon coin, on utilisera une requête POST sur l'url de l'api
# du site (cf var url_tel_img_api) avec comme corps du message l'encodage
# d'un formulaire à 3 paramètres (dont les 1ers et 3èmes param. varient
# en fonction de la page détail initiale)
# Le corps de la requête aura la forme suivante :
# list_id={param1}&app_id=leboncoin_web_utils&key={param2}
# avec param1 et param2, les 2 paramètres de l'appel à la fonction javascript
# getPhoneNumber de la page détail initiale
#
url_tel_img_api = "https://api.leboncoin.fr/api/utils/phonenumber.json"

zoe_models = ["life", "intens", "zen"]

#
# Encapsulation des fonctions requests.get et requests.post pour ajouter une tempo
# aléatoire avant l'envoi d'une requête
#
def rqGet(url, stream=False, proxies=None):
#    tempo = random.randint(1, 10)
#    time.sleep(tempo)
    result = ""
    if proxies is None:
        result = requests.get(url, stream=stream)
    else:
        result = requests.get(url, stream=stream, proxies=proxies)
    return result

def rqPost(url, data, proxies=None):
    global headers
#    tempo = random.randint(1, 10)
#    time.sleep(tempo)
    if proxies is None:
        result = requests.post(url, data=data)
    else:
        result = requests.post(url, data=data, proxies=proxies)
    return result

#
# Récupérer le parsing Soup d'une page HTML accessible via le paramètre url
#
def getSoupFromUrl(url, stream=False, proxies=None):
    request = rqGet(url, stream, proxies)
    # parse the result of the request
    soup = BeautifulSoup(request.text, 'html.parser')
    request.connection.close()
    return soup

#
# Récupérer la liste des Renault Zoe en vente pour une région donnée
#
def getRenaultZoe(region):
    global proxies
    url = url_prefix1 + region + "/?f=a&th=1&q=\"Renault+Zoe\"&it=1"
    return getSoupFromUrl(url, proxies=proxies)

#
# Dans une soup de type liste "bon coin", récupérer tous les tags <a> ayant pour parent
# un tag <div> de class css 'list-lbc' pour une region donnée
#
def getRenaultZoeList(region):
    soup = getRenaultZoe(region)
    tags = soup.find_all(lambda tag: tag.name == 'a' \
                        and tag.parent.name == 'div' \
                        and tag.parent.has_attr('class') \
                        and 'list-lbc' in tag.parent.attrs['class'])
    # ne garder que les valeurs du href sur le lien
    result = []
    for tag in tags:
        entry = {}
        entry["link"] = tag.attrs['href']
        entry["version"] = ""
        for model in zoe_models:
            if model in tag.attrs['title'].lower():
                entry["version"] = model
                entry["titre"] = tag.attrs['title']
                break
        categories = tag.find_all('div', attrs={'class': 'category'})
        if categories[0].text.strip() == '(pro)':
            entry['categorie'] = 'Professionel'
        else:
            entry['categorie'] = 'Particulier'
        result.append(entry)
    return result

#
# Récup. des paramètres de l'appel à la fct js getPhoneNumber dans une soup
# de page détail
#
def getPhoneNumberParams(soup):
    result = []
    tag_phone_params = soup.find_all(lambda tag: tag.name == 'a' \
                         and tag.has_attr('href') \
                         and 'javascript:getPhoneNumber("https://api.leboncoin.fr' in tag.attrs['href'])
    if len(tag_phone_params) > 0:
        # récupérer l'appel js complet
        call_text = tag_phone_params[0].attrs['href'].replace("\n", "")
        # parser pour récupérer les 2 derniers paramètres
        regex = re.compile("(javascript:getPhoneNumber\(\"https:\/\/api\.leboncoin.fr\")\,\ ([0-9]+)\,\ \"([0-9a-f]+)\"")
        parser = regex.search(call_text)
        result.append(str(parser.group(2)))
        result.append(str(parser.group(3)))
    return result

#
# Récupérer le lien sur l'image correspondant au numéro de telephone du vendeur
#
def getLinkPhoneImg(param1, param2):
    global headers
    res = None
    formbody = "list_id="+param1+"&app_id=leboncoin_web_utils&key="+param2
    res = rqPost(url_tel_img_api, data=formbody, proxies=proxies)
    if res.status_code == 200:
        # récupérer le champ text et le parser json
        res_js_obj = json.loads(res.text)
        if str(res_js_obj['utils']['status']) == 'OK':
            res = res_js_obj['utils']['phonenumber']
        else:
            res = ""
    return res

#
# save phone number image to disk
#
def getPhoneNumberImage(url, dest_file):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(dest_file, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    return r.status_code

#
# Mettre dans un dictionnaire toutes les propriétés d'une annonce renault zoe donnée
#
def getRenaultZoeProperties(entry):
    # récupérer la soup du détail de l'annonce ansi que les infos utiles du header
    soup = getSoupFromUrl(entry["link"])
    # afficher le titre
    tag_titre = soup.find_all(lambda tag: tag.name == 'h1' \
                         and tag.has_attr('itemprop') \
                         and 'name' in tag.attrs['itemprop'])
    print(tag_titre[0].text)
    # récupérer le prix
    tag_prix = soup.find_all(lambda tag: tag.name == 'span' \
                         and tag.has_attr('class') \
                         and 'price' in tag.attrs['class'])
    prix = tag_prix[0].attrs['content']
    entry["prix"] = int(prix)
    # récupérer l'année
    tag_annee = soup.find_all(lambda tag: tag.name == 'td' \
                         and tag.has_attr('itemprop') \
                         and 'releaseDate' in tag.attrs['itemprop'])
    annee = tag_annee[0].text.strip()
    entry["annee"] = int(annee)
    # récupérer le kilométrage
    tag_km = soup.find_all(lambda tag: tag.name == 'td' \
                         and 'KM' in tag.text)
    km = tag_km[0].text.strip()
    entry["kilometrage"] = int(re.sub("[^0-9]", "", km))
    # paramètres pour le tel vendeur
    entry["param_tel"] = getPhoneNumberParams(soup)
    if len(entry["param_tel"]) == 2:
        entry["link_tel_img"] = getLinkPhoneImg(entry["param_tel"][0], entry["param_tel"][1])
        if entry["link_tel_img"] != "":
            # save phone number image to disk
            status = getPhoneNumberImage(entry["link_tel_img"], entry["param_tel"][1]+".gif")
            entry["image"] = entry["param_tel"][1]+".gif"
            # image character recognition
            # Digits - Only Tesseract
            digits = tool.image_to_string(
                Image.open(entry["image"]),
                builder=pyocr.tesseract.DigitBuilder(7)     # mode -psm 7 pour tesseract
            )
            entry["telephone"] = str(digits)
        else:
            entry["telephone"] = ""
    else:
        entry["telephone"] = ""
    return entry

#
# Récupérer une côte par version et par année sur la centrale
#
def getCoteVersionAnnee(version, annee):
    prix = -1
    if version != "":
        url = url_prefix2+version+"+charge+rapide-"+str(annee)+".html"
        soup = getSoupFromUrl(url)
        # relever la cote
        cote = soup.find_all('span', {'class': "Result_Cote arial tx20"})
        prix = cote[0].text.strip()
        prix = int(re.sub("[^0-9]", "", prix))
    return prix

#
# colonnes du tableau
#
columns = ["region", "version", "annee", "kilometrage", "categorie", "telephone", "prix", "prix_argus"]
#
# creation du dataframe
#
autos = pd.DataFrame(columns=columns)

regions = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine" ]

for region in regions:
    print("region : %s" % region)
    tags = getRenaultZoeList(region)
    i = 0
    for tag in tags:
        print("annonce n° %d" % i)
        entry = getRenaultZoeProperties(tag)
        values = [region, entry["version"], entry["annee"], entry["kilometrage"], \
                  entry["categorie"], entry["telephone"], entry["prix"], \
                  getCoteVersionAnnee(entry["version"], entry["annee"])]
        print(values)
        autos.loc[i] = values
        i += 1

print(autos)

#annee_min = autos["annee"].min()
#annee_max = autos["annee"].max()

autos.to_csv("autos.csv")
