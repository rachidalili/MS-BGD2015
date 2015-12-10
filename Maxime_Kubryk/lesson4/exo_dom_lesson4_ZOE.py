import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

regions = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']


def cote_argus(model, year):
    url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + \
        model + '+charge+rapide-' + year + '.html'
    answer = requests.get(url)
    soup = BeautifulSoup(answer.text)

    cote = int(soup.find('span', class_='Result_Cote').get_text()[:-2].replace(" ", ""))
    #print('cote', model + " " + year + " " + cote)

    return cote


def scrap_annouce(url):
    answer = requests.get(url)
    soup = BeautifulSoup(answer.text)

    price = float(soup.find('span', class_='price').get('content'))
    print('price', price)
    # br = soup.find('div', itemprop='description').findAll('br')[-1]
    # tel = str(br.nextSibling).strip()

    text = soup.find('div', itemprop='description').get_text()
    #regex = "(0[1-9][0-9]{8}|0[1-9]([ .-/][0-9]{2}){4}|0[1-9](.[0-9]{2}){4})"
    regex = "(0[1-9]([ .-/]?[0-9]{2}){4})"

    try:
        tel = max(re.findall(regex, text)[0]).replace(" ", "").replace(".", "")
        print(re.findall(regex, text))
    except IndexError:
        tel = '...'

    print('tel', tel)

    year = int(soup.find('td', itemprop='releaseDate').get_text())
    print('year', year)

    table = soup.select('.criterias table')[0].findAll('tr')  # .find('tr > td')
    km = int(table[2].select('td')[0].get_text()[:-3].replace(" ", ""))
    print('km', km)

    return year, km, price, tel


def scrapper(regions):
    columns = ['region', 'model', 'km', 'prix', 'tel', 'argus', 'bon_plan']
    models = ['zen', 'life', 'intens']
    data = pd.DataFrame(columns=columns)

    for region in regions:
        url = "http://www.leboncoin.fr/voitures/offres/" + region + "/?f=a&th=1&q=renault+zoe"
        answer = requests.get(url)
        soup = BeautifulSoup(answer.text)

        for a in soup.findAll(lambda tag: tag.name == "a" and "title" in tag.attrs):

            try:
                announce_url = a.get('href')
                title = a.select('.lbc .detail .title')[0].get_text().lower().strip()

                if 'zoe' in title:
                    print('-------------------')
                    print(region, title)
                    year, km, price, tel = scrap_annouce(announce_url)
                    announce_data = {'region': region}
                    announce_data.update({'année': year, 'km': km, 'prix': price, 'tel': tel})
                    announce_data.update({'model': model for model in models if model in title})

                    try:
                        cote = cote_argus(announce_data['model'], str(announce_data['année']))
                        if cote >= announce_data['prix']:
                            announce_data.update({'bon_plan': 'Oui'})
                        else:
                            announce_data.update({'bon_plan': 'Non'})
                    except KeyError:
                        cote = 0
                    except ValueError:
                        cote = 0

                    announce_data.update({'argus': cote})

                    print(announce_data)

                    data = data.append(announce_data, ignore_index=True)

            except IndexError:
                print('Error')
                pass

    print(data)


scrapper(regions)
